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
