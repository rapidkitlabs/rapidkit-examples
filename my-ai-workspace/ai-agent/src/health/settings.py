"""Project shim exposing vendor health helpers for settings."""

from __future__ import annotations

import importlib.util
import os
import sys
from functools import lru_cache
from pathlib import Path
from types import ModuleType
from typing import Any, Optional

_VENDOR_MODULE = "settings"
_VENDOR_VERSION = "0.1.45"
_VENDOR_RELATIVE_PATH = "src/health/settings.py"
_VENDOR_ROOT_ENV = "RAPIDKIT_VENDOR_ROOT"
_CACHE_PREFIX = "rapidkit_vendor_settings"

DEFAULT_HEALTH_PREFIX = "/api/health/module/settings"


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

    module_name = _CACHE_PREFIX + _VENDOR_MODULE.replace("/", "_") + "_health"
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


def build_health_router(prefix: str = DEFAULT_HEALTH_PREFIX) -> Any:
    """Return a FastAPI router sourced from the vendor health runtime."""

    try:
        factory = _resolve_export("build_health_router")
    except RuntimeError:
        factory = None

    if callable(factory):
        try:
            return factory(prefix=prefix)
        except TypeError:  # pragma: no cover - factory without prefix support
            return factory()

    try:
        router = _resolve_export("router")
        if router is not None:
            return router
    except RuntimeError:
        router = None

    try:
        factory = _resolve_export("create_health_router")
    except RuntimeError:
        factory = None

    if callable(factory):
        try:
            return factory(prefix=prefix)
        except TypeError:  # pragma: no cover - factory without prefix support
            return factory()

    try:
        from fastapi import APIRouter  # type: ignore
    except ImportError:  # pragma: no cover - FastAPI optional for template rendering
        APIRouter = None  # type: ignore[assignment]

    if APIRouter is not None:
        router = APIRouter(prefix=prefix, tags=["Health", _VENDOR_MODULE])

        @router.get("/health", summary=f"{_VENDOR_MODULE} health check")
        async def read_health() -> dict[str, Any]:
            return {
                "module": _VENDOR_MODULE,
                "status": "unknown",
                "detail": "runtime not initialized",
                "warnings": [],
            }

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
            "register_settings_health expects a FastAPI application instance"
        )

    router = build_health_router()
    app.include_router(router)


try:
    register_settings_health = _resolve_export("register_settings_health")
except RuntimeError:
    register_settings_health = _fallback_register


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


__all__ = sorted(
    set(getattr(_load_vendor_module(), "__all__", []))
    | {
        "build_health_router",
        "create_health_router",
        "refresh_vendor_module",
        "register_settings_health",
        "router",
    }
)
