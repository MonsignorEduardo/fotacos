"""FastAPI application for the photo album."""

from fotacos.api.app import app
from fotacos.api.server import run_web

__all__ = ["app", "run_web"]
