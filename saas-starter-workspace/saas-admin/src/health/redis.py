"""Project shim exposing vendor health helpers for redis."""

from __future__ import annotations

import importlib.util
import os
import sys
import time
from functools import lru_cache
from pathlib import Path
from types import ModuleType
from typing import Any, Optional

_VENDOR_MODULE = "redis"
_VENDOR_VERSION = "0.1.23"
_VENDOR_RELATIVE_PATH = "src/health/redis.py"
_VENDOR_ROOT_ENV = "RAPIDKIT_VENDOR_ROOT"
_CACHE_PREFIX = "rapidkit_vendor_redis"
_STARTED_AT = time.monotonic()

DEFAULT_HEALTH_PREFIX = "/api/health/module/redis"


def _base_health_payload(*, status: str = "ok") -> dict[str, Any]:
    return {
        "module": _VENDOR_MODULE,
        "status": status,
        "version": _VENDOR_VERSION,
        "uptime": max(0.0, time.monotonic() - _STARTED_AT),
        "warnings": [],
    }


def _project_root() -> Path:
    current = Path(__file__).resolve()
    for ancestor in current.parents:
        if (ancestor / ".rapidkit").exists():
            return ancestor
        if (ancestor / "pyproject.toml").exists() or (ancestor / "package.json").exists():
            return ancestor
    return current.parents[2]


def _ensure_proxy_package(name: str, path: Path) -> None:
    if not path.exists():
        return

    original = sys.modules.get(name)
    proxy = ModuleType(name)
    if original is not None:
        proxy.__dict__.update(original.__dict__)
    proxy.__path__ = [str(path)]
    sys.modules[name] = proxy


def _vendor_module_root() -> Optional[Path]:
    """Locate the vendor module root containing <name>.py + types/ directory."""

    base = _vendor_base_dir() / "src" / "modules"
    if not base.exists():
        return None

    module_name = _VENDOR_MODULE.split("/")[-1]
    for candidate in base.rglob(f"{module_name}.py"):
        if candidate.name != f"{module_name}.py":
            continue
        if candidate.parent.name != module_name:
            continue
        return candidate.parent
    return None


def _ensure_vendor_namespaces() -> None:
    module_root = _vendor_module_root()
    if module_root is not None:
        _ensure_proxy_package("database", module_root)
        _ensure_proxy_package("types", module_root / "types")

    _ensure_proxy_package("health", _vendor_base_dir() / "src" / "health")


def _vendor_root() -> Path:
    override = os.getenv(_VENDOR_ROOT_ENV)
    if override:
        return Path(override).expanduser().resolve()
    return _project_root() / ".rapidkit" / "vendor"


def _vendor_base_dir() -> Path:
    root = _vendor_root()
    module_dir = root / _VENDOR_MODULE
    preferred = module_dir / _VENDOR_VERSION if _VENDOR_VERSION else None
    if preferred and preferred.exists():
        return preferred
    candidates = sorted(
        (path for path in module_dir.glob("*") if path.is_dir()), reverse=True
    )
    if candidates:
        return candidates[0]
    raise RuntimeError(
        "RapidKit vendor payload for '{module}' not found under {root}. Re-run `rapidkit modules install {module}`.".format(
            module=_VENDOR_MODULE,
            root=root,
        )
    )


def _vendor_file() -> Path:
    if not _VENDOR_RELATIVE_PATH:
        raise RuntimeError(
            "Vendor health relative path missing for module '{module}'. Please reinstall the module.".format(
                module=_VENDOR_MODULE,
            )
        )
    return _vendor_base_dir() / _VENDOR_RELATIVE_PATH


@lru_cache(maxsize=1)
def _load_vendor_module() -> ModuleType:
    vendor_path = _vendor_file()
    if not vendor_path.exists():
        raise RuntimeError(
            "RapidKit vendor health runtime missing at {path}. Re-run `rapidkit modules install {module}`.".format(
                path=vendor_path,
                module=_VENDOR_MODULE,
            )
        )

    _ensure_vendor_namespaces()

    vendor_base = str(_vendor_base_dir())
    if vendor_base not in sys.path:
        sys.path.insert(0, vendor_base)

    module_root = _vendor_module_root() or vendor_path.parent
    package_name = _CACHE_PREFIX + _VENDOR_MODULE.replace("/", "_") + "_pkg"
    package = sys.modules.get(package_name)
    if package is None:
        package = ModuleType(package_name)
        package.__path__ = [str(module_root)]
        sys.modules[package_name] = package
    else:
        package.__path__ = [str(module_root)]

    module_name = f"{package_name}.{vendor_path.stem}"
    spec = importlib.util.spec_from_file_location(module_name, vendor_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load vendor health runtime from {vendor_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault(module_name, module)
    spec.loader.exec_module(module)
    return module


def _resolve_export(name: str) -> Any:
    vendor = _load_vendor_module()
    try:
        return getattr(vendor, name)
    except AttributeError as exc:  # pragma: no cover - defensive guard
        raise RuntimeError(
            "Vendor health module '{module}' missing attribute '{attribute}'".format(
                module=_VENDOR_RELATIVE_PATH,
                attribute=name,
            )
        ) from exc


def refresh_vendor_module() -> None:
    """Clear import caches after vendor upgrades."""

    _load_vendor_module.cache_clear()


async def health_check() -> dict[str, Any]:
    """Return the standardized module health payload without a web router."""

    probe_names = (
        "check_health",
        "health_check",
        "module_health_status",
        f"{_VENDOR_MODULE}_health_check",
    )

    for probe_name in probe_names:
        try:
            probe = _resolve_export(probe_name)
        except Exception:
            probe = None

        if not callable(probe):
            continue

        try:
            result = probe()
            if hasattr(result, "__await__"):
                result = await result
        except Exception as exc:
            payload = _base_health_payload(status="error")
            payload["detail"] = str(exc)
            return payload

        if isinstance(result, dict):
            payload = dict(result)
            payload.setdefault("module", _VENDOR_MODULE)
            payload.setdefault("status", "ok")
            payload.setdefault("version", _VENDOR_VERSION)
            payload.setdefault("uptime", max(0.0, time.monotonic() - _STARTED_AT))
            payload.setdefault("warnings", [])
            return payload

        payload = _base_health_payload()
        payload["detail"] = str(result)
        return payload

    payload = _base_health_payload(status="unknown")
    payload["detail"] = "runtime not initialized"
    return payload


def build_health_router(prefix: str = DEFAULT_HEALTH_PREFIX) -> Any:
    """Return a standardized FastAPI router for module health.

    The route shape stays canonical for every module:
    - prefix: /api/health/module/<slug>
    - method/path: GET ""
    - tag: ["health"]
    """

    try:
        from fastapi import APIRouter  # type: ignore
    except ImportError:  # pragma: no cover - FastAPI optional for template rendering
        APIRouter = None  # type: ignore[assignment]

    if APIRouter is not None:
        router = APIRouter(prefix=prefix, tags=["health"])

        async def _build_health_payload() -> dict[str, Any]:
            return await health_check()

        @router.get("", summary=f"{_VENDOR_MODULE} health check")
        async def read_health() -> dict[str, Any]:
            return await _build_health_payload()

        @router.get("/health", include_in_schema=False)
        async def read_health_legacy() -> dict[str, Any]:
            return await _build_health_payload()

        return router

    raise RuntimeError(
        "Vendor health runtime for '{module}' does not expose a router. Regenerate the module outputs.".format(
            module=_VENDOR_MODULE,
        )
    )


def create_health_router(prefix: str = DEFAULT_HEALTH_PREFIX) -> Any:
    """Compatibility wrapper expected by integration tests."""

    return build_health_router(prefix=prefix)


def _fallback_register(app: Any) -> None:
    try:
        from fastapi import FastAPI  # type: ignore
    except ImportError:  # pragma: no cover - FastAPI optional for template rendering
        FastAPI = None  # type: ignore[assignment]

    if FastAPI is not None and not isinstance(app, FastAPI):
        raise TypeError(
            "register_redis_health expects a FastAPI application instance"
        )

    router = build_health_router()
    app.include_router(router)


try:
    register_redis_health = _resolve_export("register_redis_health")
except Exception:
    register_redis_health = _fallback_register


try:
    router = build_health_router()
except Exception:  # pragma: no cover - allow non-router health runtimes
    router = None


def __getattr__(item: str) -> Any:
    vendor = _load_vendor_module()
    try:
        return getattr(vendor, item)
    except AttributeError as exc:  # pragma: no cover - propagate helpful error
        raise AttributeError(item) from exc


try:
    _vendor_exports = set(getattr(_load_vendor_module(), "__all__", []))
except Exception:
    _vendor_exports = set()

__all__ = sorted(
    _vendor_exports
    | {
        "build_health_router",
        "create_health_router",
        "health_check",
        "refresh_vendor_module",
        "register_redis_health",
        "router",
    }
)
