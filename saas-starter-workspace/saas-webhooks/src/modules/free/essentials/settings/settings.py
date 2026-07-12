from __future__ import annotations

import importlib.util
import os
import sys
from functools import lru_cache
from pathlib import Path
from types import ModuleType
from typing import (  # noqa: F401
    Any,
    Callable,
    ClassVar,
    Iterable,
    List,
    Optional,
)

try:  # FastAPI is optional at import time; helpers validate presence before use.
    from fastapi import FastAPI
except ImportError:  # pragma: no cover - FastAPI-only utilities guard this later.
    FastAPI = None  # type: ignore[assignment]

# Compatibility shim: older vendor snapshots import BaseSettings from pydantic.
# On pydantic >=2.12 this raises an import error unless we backfill the attr.
try:
    import pydantic  # type: ignore[import-untyped]
    from pydantic.errors import PydanticImportError
    from pydantic_settings import BaseSettings as _RapidkitBaseSettingsCompat
except Exception:  # pragma: no cover - environment may lack optional deps
    pydantic = None  # type: ignore[assignment]
    PydanticImportError = None  # type: ignore[assignment]
    _RapidkitBaseSettingsCompat = None  # type: ignore[assignment]
else:
    try:
        getattr(pydantic, "BaseSettings")
    except (AttributeError, PydanticImportError):
        if _RapidkitBaseSettingsCompat is not None:
            setattr(pydantic, "BaseSettings", _RapidkitBaseSettingsCompat)


_VENDOR_MODULE = "settings"
_VENDOR_VERSION = "0.1.45"
_VENDOR_RELATIVE_PATH = "src/modules/free/essentials/settings/settings.py"
_VENDOR_ROOT_ENV = "RAPIDKIT_VENDOR_ROOT"
_VENDOR_CACHE_PREFIX = "rapidkit_vendor_"


def _project_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / ".rapidkit").is_dir():
            return parent
        if (parent / "pyproject.toml").is_file():
            return parent
    # Fallback to historical assumption (src/ is 4 levels up; project root is 5)
    try:
        return current.parents[5]
    except IndexError:
        return current.parent


def _vendor_root() -> Path:
    env_override = os.getenv(_VENDOR_ROOT_ENV)
    if env_override:
        return Path(env_override).expanduser().resolve()
    return _project_root() / ".rapidkit" / "vendor"


def _vendor_base_dir() -> Path:
    root = _vendor_root()
    base = root / _VENDOR_MODULE
    preferred = base / _VENDOR_VERSION if _VENDOR_VERSION else None
    if preferred and preferred.exists():
        return preferred
    candidates = sorted((path for path in base.glob("*") if path.is_dir()), reverse=True)
    if candidates:
        return candidates[0]
    raise RuntimeError(
        "RapidKit vendor payload for '{module}' not found under {root}. "
        "Re-run `rapidkit modules install {module}` or restore vendor snapshots.".format(
            module=_VENDOR_MODULE,
            root=root,
        )
    )


def _vendor_file() -> Path:
    return _vendor_base_dir() / _VENDOR_RELATIVE_PATH


@lru_cache(maxsize=1)
def _load_vendor_module() -> ModuleType:
    vendor_path = _vendor_file()
    if not vendor_path.exists():
        raise RuntimeError(
            "RapidKit vendor settings file missing at {path}. "
            "Re-run `rapidkit modules install {module}` to repair.".format(
                path=vendor_path,
                module=_VENDOR_MODULE,
            )
        )
    module_name = (
        _VENDOR_CACHE_PREFIX + _VENDOR_MODULE.replace("/", "_") + "_core_settings"
    )
    spec = importlib.util.spec_from_file_location(module_name, vendor_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load vendor settings module from {vendor_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault(module_name, module)
    spec.loader.exec_module(module)
    return module


_vendor = _load_vendor_module()

# Re-export vendor helpers so snippets remain compatible
Field = getattr(_vendor, "Field")
model_validator = getattr(_vendor, "model_validator")
field_validator = getattr(_vendor, "field_validator")
BaseSettings = getattr(_vendor, "BaseSettings")
SettingsConfigDict = getattr(_vendor, "SettingsConfigDict")
PydanticBaseSettingsSource = getattr(_vendor, "PydanticBaseSettingsSource")
DotEnvSettingsSource = getattr(_vendor, "DotEnvSettingsSource")
SecretsSettingsSource = getattr(_vendor, "SecretsSettingsSource")
CustomConfigSource = getattr(_vendor, "CustomConfigSource")


class Settings(getattr(_vendor, "Settings")):
    """Project wrapper around RapidKit's vendor Settings implementation.

    Extend this class to add local fields or override behaviour while keeping upstream logic
    pristine under `.rapidkit/vendor`. Fields injected by snippets land below.
    """

    # <<<inject:settings-fields>>>

    # <<<inject:settings-fields:notifications_settings_fields:start>>>

    # Notifications (Email)

    if "NOTIFICATIONS_ENABLED" in locals():
        NOTIFICATIONS_ENABLED = Field(
            default=True,
            description="Toggle notifications manager registration during startup",
        )
    else:
        NOTIFICATIONS_ENABLED: bool = Field(
            default=True,
            description="Toggle notifications manager registration during startup",
        )
    if "NOTIFICATIONS_LOG_LEVEL" in locals():
        NOTIFICATIONS_LOG_LEVEL = Field(
            default="INFO",
            description="Logging level for notifications module",
        )
    else:
        NOTIFICATIONS_LOG_LEVEL: str = Field(
            default="INFO",
            description="Logging level for notifications module",
        )
    if "NOTIFICATIONS_SMTP_HOST" in locals():
        NOTIFICATIONS_SMTP_HOST = Field(
            default="localhost",
            description="SMTP host used for outbound email",
        )
    else:
        NOTIFICATIONS_SMTP_HOST: str = Field(
            default="localhost",
            description="SMTP host used for outbound email",
        )
    if "NOTIFICATIONS_SMTP_PORT" in locals():
        NOTIFICATIONS_SMTP_PORT = Field(
            default=587,
            description="SMTP port used for outbound email",
        )
    else:
        NOTIFICATIONS_SMTP_PORT: int = Field(
            default=587,
            description="SMTP port used for outbound email",
        )
    if "NOTIFICATIONS_SMTP_USERNAME" in locals():
        NOTIFICATIONS_SMTP_USERNAME = Field(
            default=None,
            description="Optional SMTP username",
        )
    else:
        NOTIFICATIONS_SMTP_USERNAME: Optional[str] = Field(
            default=None,
            description="Optional SMTP username",
        )
    if "NOTIFICATIONS_SMTP_PASSWORD" in locals():
        NOTIFICATIONS_SMTP_PASSWORD = Field(
            default=None,
            description="Optional SMTP password",
        )
    else:
        NOTIFICATIONS_SMTP_PASSWORD: Optional[str] = Field(
            default=None,
            description="Optional SMTP password",
        )
    if "NOTIFICATIONS_SMTP_USE_TLS" in locals():
        NOTIFICATIONS_SMTP_USE_TLS = Field(
            default=True,
            description="Use STARTTLS when connecting to SMTP",
        )
    else:
        NOTIFICATIONS_SMTP_USE_TLS: bool = Field(
            default=True,
            description="Use STARTTLS when connecting to SMTP",
        )
    if "NOTIFICATIONS_SMTP_TIMEOUT" in locals():
        NOTIFICATIONS_SMTP_TIMEOUT = Field(
            default=30,
            description="Socket timeout (seconds) for SMTP operations",
        )
    else:
        NOTIFICATIONS_SMTP_TIMEOUT: float = Field(
            default=30,
            description="Socket timeout (seconds) for SMTP operations",
        )
    if "NOTIFICATIONS_SENDER_FROM_EMAIL" in locals():
        NOTIFICATIONS_SENDER_FROM_EMAIL = Field(
            default="noreply@rapidkit.local",
            description="Default From email address",
        )
    else:
        NOTIFICATIONS_SENDER_FROM_EMAIL: str = Field(
            default="noreply@rapidkit.local",
            description="Default From email address",
        )
    if "NOTIFICATIONS_SENDER_FROM_NAME" in locals():
        NOTIFICATIONS_SENDER_FROM_NAME = Field(
            default="RapidKit Notifications",
            description="Human readable From name",
        )
    else:
        NOTIFICATIONS_SENDER_FROM_NAME: Optional[str] = Field(
            default="RapidKit Notifications",
            description="Human readable From name",
        )
    if "NOTIFICATIONS_SENDER_REPLY_TO" in locals():
        NOTIFICATIONS_SENDER_REPLY_TO = Field(
            default=None,
            description="Optional Reply-To address",
        )
    else:
        NOTIFICATIONS_SENDER_REPLY_TO: Optional[str] = Field(
            default=None,
            description="Optional Reply-To address",
        )
    if "NOTIFICATIONS_TEMPLATE_DIRECTORY" in locals():
        NOTIFICATIONS_TEMPLATE_DIRECTORY = Field(
            default="./templates/notifications",
            description="Path to notifications email templates",
        )
    else:
        NOTIFICATIONS_TEMPLATE_DIRECTORY: str = Field(
            default="./templates/notifications",
            description="Path to notifications email templates",
        )
    if "NOTIFICATIONS_TEMPLATE_AUTO_RELOAD" in locals():
        NOTIFICATIONS_TEMPLATE_AUTO_RELOAD = Field(
            default=False,
            description="Reload templates on every render (development)",
        )
    else:
        NOTIFICATIONS_TEMPLATE_AUTO_RELOAD: bool = Field(
            default=False,
            description="Reload templates on every render (development)",
        )
    if "NOTIFICATIONS_RETRY_MAX_ATTEMPTS" in locals():
        NOTIFICATIONS_RETRY_MAX_ATTEMPTS = Field(
            default=3,
            description="Maximum email retry attempts",
        )
    else:
        NOTIFICATIONS_RETRY_MAX_ATTEMPTS: int = Field(
            default=3,
            description="Maximum email retry attempts",
        )
    if "NOTIFICATIONS_RETRY_BACKOFF_SECONDS" in locals():
        NOTIFICATIONS_RETRY_BACKOFF_SECONDS = Field(
            default=2.0,
            description="Exponential backoff multiplier in seconds",
        )
    else:
        NOTIFICATIONS_RETRY_BACKOFF_SECONDS: float = Field(
            default=2.0,
            description="Exponential backoff multiplier in seconds",
        )
    if "NOTIFICATIONS_RETRY_INITIAL_DELAY_SECONDS" in locals():
        NOTIFICATIONS_RETRY_INITIAL_DELAY_SECONDS = Field(
            default=1.0,
            description="Initial retry delay in seconds",
        )
    else:
        NOTIFICATIONS_RETRY_INITIAL_DELAY_SECONDS: float = Field(
            default=1.0,
            description="Initial retry delay in seconds",
        )
    if "NOTIFICATIONS_RATE_LIMIT_ENABLED" in locals():
        NOTIFICATIONS_RATE_LIMIT_ENABLED = Field(
            default=False,
            description="Expose rate limiting metadata in health output",
        )
    else:
        NOTIFICATIONS_RATE_LIMIT_ENABLED: bool = Field(
            default=False,
            description="Expose rate limiting metadata in health output",
        )
    if "NOTIFICATIONS_RATE_LIMIT_MAX_PER_MINUTE" in locals():
        NOTIFICATIONS_RATE_LIMIT_MAX_PER_MINUTE = Field(
            default=None,
            description="Optional notifications per minute cap",
        )
    else:
        NOTIFICATIONS_RATE_LIMIT_MAX_PER_MINUTE: Optional[int] = Field(
            default=None,
            description="Optional notifications per minute cap",
        )
    if "NOTIFICATIONS_RATE_LIMIT_MAX_PER_HOUR" in locals():
        NOTIFICATIONS_RATE_LIMIT_MAX_PER_HOUR = Field(
            default=None,
            description="Optional notifications per hour cap",
        )
    else:
        NOTIFICATIONS_RATE_LIMIT_MAX_PER_HOUR: Optional[int] = Field(
            default=None,
            description="Optional notifications per hour cap",
        )

    # <<<inject:settings-fields:notifications_settings_fields:end>>>

    # <<<inject:settings-fields:redis_settings_fields:start>>>

    # Cache (Redis)

    if "REDIS_URL" in locals():
        REDIS_URL = Field(
            default="redis://localhost:6379/0",
            description="Redis connection URL (overrides individual host settings when provided)",
        )
    else:
        REDIS_URL: Optional[str] = Field(
            default="redis://localhost:6379/0",
            description="Redis connection URL (overrides individual host settings when provided)",
        )
    if "REDIS_HOST" in locals():
        REDIS_HOST = Field(
            default="localhost",
            description="Redis host used when REDIS_URL is absent",
        )
    else:
        REDIS_HOST: str = Field(
            default="localhost",
            description="Redis host used when REDIS_URL is absent",
        )
    if "REDIS_PORT" in locals():
        REDIS_PORT = Field(
            default=6379,
            description="Redis port when building the URL dynamically",
        )
    else:
        REDIS_PORT: int = Field(
            default=6379,
            description="Redis port when building the URL dynamically",
        )
    if "REDIS_DB" in locals():
        REDIS_DB = Field(
            default=0,
            description="Redis database index",
        )
    else:
        REDIS_DB: int = Field(
            default=0,
            description="Redis database index",
        )
    if "REDIS_PASSWORD" in locals():
        REDIS_PASSWORD = Field(
            default="",
            description="Redis password",
        )
    else:
        REDIS_PASSWORD: Optional[str] = Field(
            default="",
            description="Redis password",
        )
    if "REDIS_USE_TLS" in locals():
        REDIS_USE_TLS = Field(
            default=False,
            description="Use TLS (rediss://) when composing the URL",
        )
    else:
        REDIS_USE_TLS: bool = Field(
            default=False,
            description="Use TLS (rediss://) when composing the URL",
        )
    if "REDIS_PRECONNECT" in locals():
        REDIS_PRECONNECT = Field(
            default=False,
            description="Attempt to connect to Redis during application startup",
        )
    else:
        REDIS_PRECONNECT: bool = Field(
            default=False,
            description="Attempt to connect to Redis during application startup",
        )
    if "REDIS_CONNECT_RETRIES" in locals():
        REDIS_CONNECT_RETRIES = Field(
            default=3,
            description="Number of connection retries for async client initialisation",
        )
    else:
        REDIS_CONNECT_RETRIES: int = Field(
            default=3,
            description="Number of connection retries for async client initialisation",
        )
    if "REDIS_CONNECT_BACKOFF_BASE" in locals():
        REDIS_CONNECT_BACKOFF_BASE = Field(
            default=0.5,
            description="Base backoff delay (seconds) for retry attempts",
        )
    else:
        REDIS_CONNECT_BACKOFF_BASE: float = Field(
            default=0.5,
            description="Base backoff delay (seconds) for retry attempts",
        )
    if "CACHE_TTL" in locals():
        CACHE_TTL = Field(
            default=3600,
            description="Default cache TTL used by helpers",
        )
    else:
        CACHE_TTL: int = Field(
            default=3600,
            description="Default cache TTL used by helpers",
        )

    # <<<inject:settings-fields:redis_settings_fields:end>>>

    # <<<inject:settings-fields:db_postgres_settings_fields:start>>>

    # PostgreSQL overrides
    if "DB_POOL_SIZE" in locals():
        DB_POOL_SIZE = Field(
            default=10,
            description="Primary size of the SQLAlchemy connection pool",
        )
    else:
        DB_POOL_SIZE: int = Field(
            default=10,
            description="Primary size of the SQLAlchemy connection pool",
        )
    if "DB_MAX_OVERFLOW" in locals():
        DB_MAX_OVERFLOW = Field(
            default=20,
            description="Maximum overflow connections allowed beyond the pool size",
        )
    else:
        DB_MAX_OVERFLOW: int = Field(
            default=20,
            description="Maximum overflow connections allowed beyond the pool size",
        )
    if "DB_POOL_RECYCLE" in locals():
        DB_POOL_RECYCLE = Field(
            default=3600,
            description="Seconds before recycling idle connections to avoid stale sessions",
        )
    else:
        DB_POOL_RECYCLE: int = Field(
            default=3600,
            description="Seconds before recycling idle connections to avoid stale sessions",
        )
    if "DB_POOL_TIMEOUT" in locals():
        DB_POOL_TIMEOUT = Field(
            default=30,
            description="Seconds to wait for an available connection from the pool",
        )
    else:
        DB_POOL_TIMEOUT: int = Field(
            default=30,
            description="Seconds to wait for an available connection from the pool",
        )
    if "DB_ECHO" in locals():
        DB_ECHO = Field(
            default=False,
            description="Enable SQLAlchemy echo logging for debugging",
        )
    else:
        DB_ECHO: bool = Field(
            default=False,
            description="Enable SQLAlchemy echo logging for debugging",
        )
    if "DB_EXPIRE_ON_COMMIT" in locals():
        DB_EXPIRE_ON_COMMIT = Field(
            default=False,
            description="Expire ORM objects on commit (disable for better performance)",
        )
    else:
        DB_EXPIRE_ON_COMMIT: bool = Field(
            default=False,
            description="Expire ORM objects on commit (disable for better performance)",
        )
    if "DATABASE_URL" in locals():
        DATABASE_URL = Field(
            default="postgresql://postgres:postgres@localhost:5432/myapp",
            description="Primary PostgreSQL connection string",
        )
    else:
        DATABASE_URL: str = Field(
            default="postgresql://postgres:postgres@localhost:5432/myapp",
            description="Primary PostgreSQL connection string",
        )
    if "TEST_DATABASE_URL" in locals():
        TEST_DATABASE_URL = Field(
            default="postgresql://postgres:postgres@localhost:5432/myapp_test",
            description="Optional test database connection string",
        )
    else:
        TEST_DATABASE_URL: Optional[str] = Field(
            default="postgresql://postgres:postgres@localhost:5432/myapp_test",
            description="Optional test database connection string",
        )

    # <<<inject:settings-fields:db_postgres_settings_fields:end>>>

    # <<<inject:settings-fields:logging_settings_fields:start>>>

    LOG_LEVEL: str = Field(default="INFO", description="Default log level (DEBUG|INFO|WARNING|ERROR|CRITICAL)")
    LOG_FORMAT: str = Field(default="json", description="Log format (json|text|colored)")
    ENABLE_CORRELATION_IDS: bool = Field(default=True, description="Enable request/trace correlation IDs")
    CORRELATION_ID_HEADER: str = Field(default="X-Request-ID", description="Header used/provided for correlation ID")
    ENABLE_USER_CONTEXT: bool = Field(default=True, description="Capture user id context in logs if available")
    ENABLE_SAMPLING: bool = Field(default=False, description="Enable probabilistic sampling of DEBUG logs")
    LOG_SAMPLING_RATE: float = Field(default=0.1, description="Sampling rate (0-1) for DEBUG logs")
    LOG_SINKS: List[str] = Field(default_factory=lambda: ["stderr"], description="Enabled sinks (stderr,file,syslog,queue)")
    LOG_FILE_PATH: str = Field(default="logs/app.log", description="File path when file sink enabled")
    FILE_ROTATE: bool = Field(default=True, description="Rotate file logs (size/time based)")
    LOG_ENABLE_REDACTION: bool = Field(default=True, description="Redact sensitive tokens/secrets from messages")
    JSON_INDENT: int = Field(default=0, description="Indent level for JSON logs (0=compact)")
    LOG_ASYNC_QUEUE: bool = Field(default=True, description="Use async queue (standard for non-blocking dispatch)")
    OTEL_BRIDGE_ENABLED: bool = Field(default=False, description="Forward logs to OpenTelemetry bridge (stub)")
    METRICS_BRIDGE_ENABLED: bool = Field(default=False, description="Emit metrics counters/timers for log events (stub)")

    # <<<inject:settings-fields:logging_settings_fields:end>>>
    # Dynamic snippets injected here


# Resolve typing forward references introduced by snippet injections.
Settings.model_rebuild()


try:  # Apply optional override contracts when available
    from src.services.override_contracts import apply_module_overrides
except ImportError:  # pragma: no cover - decorator support is optional at runtime
    apply_module_overrides = None

if apply_module_overrides is not None:
    apply_module_overrides(Settings, "settings")


@lru_cache()
def get_settings() -> Settings:
    return Settings()


def settings_dependency() -> Settings:
    """Dependency hook for FastAPI routes (`Depends(settings_dependency)`)."""

    return get_settings()


def _assert_fastapi() -> None:
    if FastAPI is None:  # pragma: no cover - exercised only without fastapi installed
        raise RuntimeError(
            "FastAPI is not installed. Install `fastapi` to use integration helpers."
        )


def configure_fastapi_app(
    app: "FastAPI",
    *,
    state_namespace: str = "settings",
    dependency_targets: Optional[Iterable[Callable[..., Any]]] = None,
) -> Settings:
    """Attach settings to the FastAPI application and register dependency overrides.

    Parameters
    ----------
    app:
        FastAPI application instance.
    state_namespace:
        Attribute on `app.state` where the resolved settings instance is stored.
    dependency_targets:
        Iterable of callables to override with :func:`settings_dependency`. By default the
        overrides target both :func:`get_settings` and :func:`settings_dependency` to match
        common usage patterns.
    """

    _assert_fastapi()

    settings = get_settings()
    if state_namespace:
        setattr(app.state, state_namespace, settings)

    overrides = getattr(app, "dependency_overrides", None)
    if overrides is not None:
        targets = tuple(dependency_targets or (get_settings, settings_dependency))
        for target in targets:
            overrides.setdefault(target, settings_dependency)

    return settings


@lru_cache(maxsize=1)
def get_settings_state_key(default: str = "settings") -> str:
    """Provide a consistent state key for applications sharing the module."""

    return default


def refresh_vendor_settings() -> None:
    """Force a reload of the vendor module (helpful after upgrades)."""

    _load_vendor_module.cache_clear()
    _load_vendor_module()


settings = get_settings()


__all__ = [
    "Settings",
    "get_settings",
    "settings",
    "settings_dependency",
    "configure_fastapi_app",
    "get_settings_state_key",
    "refresh_vendor_settings",
    "CustomConfigSource",
    "Field",
    "model_validator",
    "field_validator",
    "BaseSettings",
    "SettingsConfigDict",
    "PydanticBaseSettingsSource",
    "DotEnvSettingsSource",
    "SecretsSettingsSource",
]
