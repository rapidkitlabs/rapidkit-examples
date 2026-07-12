"""SaaS starter routes composed from installed RapidKit modules."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel, EmailStr, Field

from src.modules.free.auth.core.auth.core import AuthCoreRuntime
from src.modules.free.auth.core.auth.dependencies import get_auth_core_runtime
from src.modules.free.auth.oauth.oauth import OAuthRuntime
from src.modules.free.auth.oauth.oauth import get_runtime as get_oauth_runtime
from src.modules.free.auth.session.session import SessionRuntime
from src.modules.free.auth.session.session import get_runtime as get_session_runtime
from src.modules.free.security.rate_limiting.dependencies import rate_limit_dependency
from src.modules.free.users.users_core.core.users.dependencies import get_users_service
from src.modules.free.users.users_core.core.users.dto import UserCreateDTO, UserDTO
from src.modules.free.users.users_core.core.users.errors import (
    UserEmailConflictError,
    UserNotFoundError,
)
from src.modules.free.users.users_core.core.users.service import UsersService
from src.modules.free.users.users_profiles.core.users.profiles.dependencies import (
    get_user_profile_service_facade,
)
from src.modules.free.users.users_profiles.core.users.profiles.dto import (
    UserProfileReadDTO,
    UserProfileUpdateDTO,
)
from src.modules.free.users.users_profiles.core.users.profiles.errors import (
    ProfileNotFoundError,
    ProfileValidationError,
)
from src.modules.free.users.users_profiles.core.users.profiles.service import (
    UserProfileServiceFacade,
)

router = APIRouter(tags=["saas-api"])


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=200)
    full_name: str | None = Field(default=None, max_length=200)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=200)


class OAuthCallbackRequest(BaseModel):
    state: str = Field(min_length=8)
    email: EmailStr | None = None
    full_name: str | None = Field(default=None, max_length=200)


class PaymentMethodRequest(BaseModel):
    type: str = Field(default="card", max_length=40)
    provider: str = Field(default="stripe", max_length=40)
    last4: str = Field(min_length=4, max_length=4)
    exp_month: int = Field(ge=1, le=12)
    exp_year: int = Field(ge=2024, le=2100)


class TeamCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)


class CheckoutRequest(BaseModel):
    plan_id: str = Field(min_length=2, max_length=60)


@dataclass(slots=True)
class InMemoryBillingStore:
    plans: list[dict[str, Any]]
    subscriptions_by_user: dict[str, dict[str, Any]]
    payment_methods_by_user: dict[str, list[dict[str, Any]]]
    teams_by_user: dict[str, list[dict[str, Any]]]


_STORE = InMemoryBillingStore(
    plans=[
        {
            "id": "starter",
            "name": "Starter",
            "price_monthly": 19,
            "currency": "usd",
            "features": ["1 workspace", "5 members", "Email support"],
        },
        {
            "id": "growth",
            "name": "Growth",
            "price_monthly": 79,
            "currency": "usd",
            "features": ["10 workspaces", "25 members", "Priority support"],
        },
        {
            "id": "scale",
            "name": "Scale",
            "price_monthly": 249,
            "currency": "usd",
            "features": ["Unlimited workspaces", "Unlimited members", "SLA + SSO"],
        },
    ],
    subscriptions_by_user={},
    payment_methods_by_user={},
    teams_by_user={},
)


def _utcnow_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


async def _get_session_runtime() -> SessionRuntime:
    try:
        return await get_session_runtime()
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Session module is not configured. Set RAPIDKIT_SESSION_SECRET.",
        ) from exc


def _set_session_cookie(response: Response, runtime: SessionRuntime, token: str, expires_at: float) -> None:
    cookie = runtime.settings.cookie
    response.set_cookie(
        key=cookie.name,
        value=token,
        domain=cookie.domain,
        secure=cookie.secure,
        httponly=cookie.httponly,
        samesite=cookie.same_site,
        expires=int(expires_at),
    )


async def _get_current_user(
    request: Request,
    users_service: UsersService,
    auth_runtime: AuthCoreRuntime,
    session_runtime: SessionRuntime,
) -> UserDTO:
    user_id: str | None = None
    auth_header = request.headers.get("authorization")

    if auth_header and auth_header.lower().startswith("bearer "):
        bearer_token = auth_header.split(" ", 1)[1]
        try:
            payload = auth_runtime.verify_token(bearer_token)
            user_id = str(payload.get("sub", ""))
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    else:
        session_token = request.cookies.get(session_runtime.settings.cookie.name)
        if not session_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required",
            )
        try:
            session = session_runtime.verify_session_token(session_token)
            user_id = session.user_id
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth context")

    try:
        return UserDTO.from_entity(await users_service.get_user(user_id))
    except UserNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterRequest,
    response: Response,
    users_service: UsersService = Depends(get_users_service),
    auth_runtime: AuthCoreRuntime = Depends(get_auth_core_runtime),
    _: Any = Depends(rate_limit_dependency(rule="default", cost=1)),
) -> dict[str, Any]:
    try:
        password_hash = auth_runtime.hash_password(payload.password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

    try:
        user = await users_service.create_user(
            UserCreateDTO(
                email=payload.email,
                full_name=payload.full_name,
                is_verified=False,
                metadata={"password_hash": password_hash, "auth_provider": "local"},
            )
        )
    except UserEmailConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    session_runtime = await _get_session_runtime()
    access_token = auth_runtime.issue_token(
        str(user.id),
        scopes=["user:read", "user:write", "billing:read", "team:write"],
        custom_claims={"email": str(user.email)},
    )
    session_envelope = session_runtime.issue_session(
        str(user.id),
        payload={"email": str(user.email), "auth_method": "password"},
    )
    _set_session_cookie(response, session_runtime, session_envelope.token, session_envelope.session.expires_at)

    return {
        "user": UserDTO.from_entity(user).model_dump(mode="json"),
        "access_token": access_token,
        "token_type": "bearer",
        "session_id": session_envelope.session.session_id,
        "refresh_token": session_envelope.refresh_token,
    }


@router.post("/auth/login")
async def login(
    payload: LoginRequest,
    response: Response,
    users_service: UsersService = Depends(get_users_service),
    auth_runtime: AuthCoreRuntime = Depends(get_auth_core_runtime),
    _: Any = Depends(rate_limit_dependency(rule="default", cost=1)),
) -> dict[str, Any]:
    try:
        user = await users_service.get_user_by_email(payload.email)
    except UserNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials") from exc

    password_hash = (user.metadata or {}).get("password_hash") if user.metadata else None
    if not password_hash or not auth_runtime.verify_password(payload.password, password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    session_runtime = await _get_session_runtime()
    access_token = auth_runtime.issue_token(
        str(user.id),
        scopes=["user:read", "user:write", "billing:read", "team:write"],
        custom_claims={"email": str(user.email)},
    )
    session_envelope = session_runtime.issue_session(
        str(user.id),
        payload={"email": str(user.email), "auth_method": "password"},
    )
    _set_session_cookie(response, session_runtime, session_envelope.token, session_envelope.session.expires_at)

    return {
        "user": UserDTO.from_entity(user).model_dump(mode="json"),
        "access_token": access_token,
        "token_type": "bearer",
        "session_id": session_envelope.session.session_id,
        "refresh_token": session_envelope.refresh_token,
    }


@router.get("/auth/oauth/{provider}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def oauth_authorize(
    provider: str,
    request: Request,
    oauth_runtime: OAuthRuntime = Depends(get_oauth_runtime),
) -> Response:
    callback_url = str(request.url_for("oauth_callback", provider=provider))
    try:
        redirect_url = oauth_runtime.build_authorize_url(
            provider,
            redirect_override=callback_url,
            metadata={
                "ip": request.client.host if request.client else None,
                "user_agent": request.headers.get("user-agent"),
            },
        )
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"OAuth provider '{provider}' is not configured",
        ) from exc

    response = Response(status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    response.headers["Location"] = redirect_url
    return response


@router.post("/auth/oauth/{provider}/callback")
async def oauth_callback(
    provider: str,
    payload: OAuthCallbackRequest,
    response: Response,
    users_service: UsersService = Depends(get_users_service),
    auth_runtime: AuthCoreRuntime = Depends(get_auth_core_runtime),
    oauth_runtime: OAuthRuntime = Depends(get_oauth_runtime),
) -> dict[str, Any]:
    try:
        oauth_runtime.validate_callback(provider, payload.state)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    resolved_email = payload.email or EmailStr(f"{provider}_{payload.state[:10]}@oauth.local")

    try:
        user = await users_service.get_user_by_email(resolved_email)
    except UserNotFoundError:
        user = await users_service.create_user(
            UserCreateDTO(
                email=resolved_email,
                full_name=payload.full_name,
                is_verified=True,
                metadata={"auth_provider": provider},
            )
        )

    session_runtime = await _get_session_runtime()
    access_token = auth_runtime.issue_token(
        str(user.id),
        scopes=["user:read", "user:write", "billing:read", "team:write"],
        custom_claims={"email": str(user.email), "provider": provider},
    )
    session_envelope = session_runtime.issue_session(
        str(user.id),
        payload={"email": str(user.email), "auth_method": f"oauth:{provider}"},
    )
    _set_session_cookie(response, session_runtime, session_envelope.token, session_envelope.session.expires_at)

    return {
        "user": UserDTO.from_entity(user).model_dump(mode="json"),
        "access_token": access_token,
        "token_type": "bearer",
        "session_id": session_envelope.session.session_id,
        "refresh_token": session_envelope.refresh_token,
        "provider": provider,
    }


@router.get("/auth/me")
async def auth_me(
    request: Request,
    users_service: UsersService = Depends(get_users_service),
    auth_runtime: AuthCoreRuntime = Depends(get_auth_core_runtime),
) -> dict[str, Any]:
    session_runtime = await _get_session_runtime()
    user = await _get_current_user(request, users_service, auth_runtime, session_runtime)
    return {"user": user.model_dump(mode="json")}


@router.get("/users/profile", response_model=UserProfileReadDTO)
async def get_current_user_profile(
    request: Request,
    users_service: UsersService = Depends(get_users_service),
    auth_runtime: AuthCoreRuntime = Depends(get_auth_core_runtime),
    profile_facade: UserProfileServiceFacade = Depends(get_user_profile_service_facade),
) -> UserProfileReadDTO:
    session_runtime = await _get_session_runtime()
    user = await _get_current_user(request, users_service, auth_runtime, session_runtime)
    try:
        return await profile_facade.get_profile(user.id)
    except ProfileNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.put("/users/profile", response_model=UserProfileReadDTO)
async def upsert_current_user_profile(
    payload: UserProfileUpdateDTO,
    request: Request,
    users_service: UsersService = Depends(get_users_service),
    auth_runtime: AuthCoreRuntime = Depends(get_auth_core_runtime),
    profile_facade: UserProfileServiceFacade = Depends(get_user_profile_service_facade),
) -> UserProfileReadDTO:
    session_runtime = await _get_session_runtime()
    user = await _get_current_user(request, users_service, auth_runtime, session_runtime)
    try:
        return await profile_facade.upsert_profile(user.id, payload)
    except ProfileValidationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc


@router.get("/subscriptions/plans")
async def list_subscription_plans() -> dict[str, Any]:
    return {"plans": _STORE.plans}


@router.post("/subscriptions/checkout", status_code=status.HTTP_201_CREATED)
async def create_subscription_checkout(
    payload: CheckoutRequest,
    request: Request,
    users_service: UsersService = Depends(get_users_service),
    auth_runtime: AuthCoreRuntime = Depends(get_auth_core_runtime),
    _: Any = Depends(rate_limit_dependency(rule="default", cost=1)),
) -> dict[str, Any]:
    session_runtime = await _get_session_runtime()
    user = await _get_current_user(request, users_service, auth_runtime, session_runtime)

    selected_plan = next((plan for plan in _STORE.plans if plan["id"] == payload.plan_id), None)
    if selected_plan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")

    subscription = {
        "user_id": user.id,
        "plan": selected_plan,
        "status": "active",
        "started_at": _utcnow_iso(),
    }
    _STORE.subscriptions_by_user[user.id] = subscription
    return {"checkout": subscription}


@router.get("/subscriptions/current")
async def get_current_subscription(
    request: Request,
    users_service: UsersService = Depends(get_users_service),
    auth_runtime: AuthCoreRuntime = Depends(get_auth_core_runtime),
) -> dict[str, Any]:
    session_runtime = await _get_session_runtime()
    user = await _get_current_user(request, users_service, auth_runtime, session_runtime)
    current = _STORE.subscriptions_by_user.get(user.id)
    if current is None:
        return {"subscription": None}
    return {"subscription": current}


@router.post("/billing/payment-method", status_code=status.HTTP_201_CREATED)
async def add_payment_method(
    payload: PaymentMethodRequest,
    request: Request,
    users_service: UsersService = Depends(get_users_service),
    auth_runtime: AuthCoreRuntime = Depends(get_auth_core_runtime),
    _: Any = Depends(rate_limit_dependency(rule="default", cost=1)),
) -> dict[str, Any]:
    session_runtime = await _get_session_runtime()
    user = await _get_current_user(request, users_service, auth_runtime, session_runtime)
    methods = _STORE.payment_methods_by_user.setdefault(user.id, [])
    method = {
        "id": f"pm_{len(methods) + 1}",
        "type": payload.type,
        "provider": payload.provider,
        "last4": payload.last4,
        "exp_month": payload.exp_month,
        "exp_year": payload.exp_year,
        "created_at": _utcnow_iso(),
    }
    methods.append(method)
    return {"payment_method": method}


@router.get("/teams")
async def list_teams(
    request: Request,
    users_service: UsersService = Depends(get_users_service),
    auth_runtime: AuthCoreRuntime = Depends(get_auth_core_runtime),
) -> dict[str, Any]:
    session_runtime = await _get_session_runtime()
    user = await _get_current_user(request, users_service, auth_runtime, session_runtime)
    return {"teams": _STORE.teams_by_user.get(user.id, [])}


@router.post("/teams", status_code=status.HTTP_201_CREATED)
async def create_team(
    payload: TeamCreateRequest,
    request: Request,
    users_service: UsersService = Depends(get_users_service),
    auth_runtime: AuthCoreRuntime = Depends(get_auth_core_runtime),
    _: Any = Depends(rate_limit_dependency(rule="default", cost=1)),
) -> dict[str, Any]:
    session_runtime = await _get_session_runtime()
    user = await _get_current_user(request, users_service, auth_runtime, session_runtime)

    bucket = _STORE.teams_by_user.setdefault(user.id, [])
    team = {
        "id": f"team_{len(bucket) + 1}",
        "name": payload.name,
        "owner_user_id": user.id,
        "created_at": _utcnow_iso(),
    }
    bucket.append(team)
    return {"team": team}


__all__ = ["router"]
