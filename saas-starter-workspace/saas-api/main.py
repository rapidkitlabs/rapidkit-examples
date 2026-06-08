"""ASGI entrypoint shim for tooling and deployment probes."""

from src.main import app

__all__ = ["app"]
