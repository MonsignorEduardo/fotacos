"""FastAPI application configuration and setup."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from fotacos.api.routes import photos

# Project root and paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
IMGS_DIR = PROJECT_ROOT / "imgs"
THUMBNAILS_DIR = IMGS_DIR / "thumbnails"
WEB_DIST_DIR = PROJECT_ROOT / "src" / "web" / "dist"

# Ensure directories exist
IMGS_DIR.mkdir(exist_ok=True)
THUMBNAILS_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title="Fotacos API",
    description="Photo album API for managing and serving photos",
    version="0.0.1",
)

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(photos.router, prefix="/api")

# Mount static files for images
app.mount("/imgs", StaticFiles(directory=IMGS_DIR), name="imgs")

# Mount the built web app (production)
if WEB_DIST_DIR.exists():
    app.mount("/", StaticFiles(directory=WEB_DIST_DIR, html=True), name="web")
