"""FastAPI application configuration and setup."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger

from fotacos.api.routes import photos
from fotacos.database import close_db, init_db
from fotacos.env import get_settings
from fotacos.logging_config import setup_logging

setup_logging()
settings = get_settings()

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
WEB_DIST_DIR = PROJECT_ROOT / "src" / "web" / "dist"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown."""
    logger.info("Starting Fotacos API application")
    settings.ensure_directories()
    logger.debug("Ensured upload directories exist")
    await init_db()
    logger.info("Database initialized successfully")
    yield
    logger.info("Shutting down Fotacos API application")
    await close_db()
    logger.info("Database connection closed")


app = FastAPI(
    title="Fotacos API",
    description="Photo album API for managing and serving photos",
    version="0.0.1",
    lifespan=lifespan,
)

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,  # type: ignore[arg-type]
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(photos.router, prefix="/api")

# Mount public directory for photos and thumbnails
app.mount("/public", StaticFiles(directory=settings.upload_dir.parent), name="public")

# Mount the built web app (production)
if WEB_DIST_DIR.exists():
    app.mount("/", StaticFiles(directory=WEB_DIST_DIR, html=True), name="web")
