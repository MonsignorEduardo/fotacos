"""Photo management API routes."""

import uuid
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile
from loguru import logger
from pydantic import BaseModel

from fotacos.env import get_settings
from fotacos.models import Photo
from fotacos.services import convert_to_webp, generate_thumbnail

settings = get_settings()

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}

router = APIRouter(tags=["photos"])


class PhotoResponse(BaseModel):
    """Response model for a photo."""

    id: int
    filename: str
    original_url: str
    thumbnail_url: str
    file_size: int
    created_at: str


class PhotoListResponse(BaseModel):
    """Response model for listing photos."""

    photos: list[PhotoResponse]
    total: int


@router.get("/photos", response_model=PhotoListResponse)
async def list_photos() -> PhotoListResponse:
    """List all photos from the database."""
    logger.info("Fetching all photos from database")
    photos = await Photo.all().order_by("-created_at")

    photo_responses = [
        PhotoResponse(
            id=photo.id,
            filename=photo.filename,
            original_url=photo.original_url,
            thumbnail_url=photo.thumbnail_url,
            file_size=photo.file_size,
            created_at=photo.created_at.isoformat(),
        )
        for photo in photos
    ]

    logger.debug(f"Retrieved {len(photo_responses)} photos")
    return PhotoListResponse(photos=photo_responses, total=len(photo_responses))


@router.post("/photos", response_model=PhotoResponse)
async def upload_photo(file: Annotated[UploadFile, File(description="Photo file to upload")]) -> PhotoResponse:
    """Upload a new photo, generate thumbnail, and save to database."""
    logger.info(f"Received photo upload request: {file.filename}")

    if not file.filename:
        logger.warning("Upload attempt with no filename")
        raise HTTPException(status_code=400, detail="No filename provided")

    # Validate extension
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        logger.warning(f"Invalid file extension attempted: {ext} for file {file.filename}")
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    # Validate MIME type
    if not file.content_type or not file.content_type.startswith("image/"):
        logger.warning(f"Invalid MIME type: {file.content_type} for file {file.filename}")
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")

    unique_id = uuid.uuid4()
    webp_filename = f"photo_{unique_id}.webp"
    logger.debug(f"Generated unique filename: {webp_filename}")

    full_photo_path = settings.upload_dir / webp_filename
    thumbnail_photo_path = settings.upload_dir / "thumbnails" / webp_filename

    # Ensure directories exist
    full_photo_path.parent.mkdir(parents=True, exist_ok=True)
    thumbnail_photo_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        logger.debug("Converting image to WebP format")
        # Convert original to WebP
        webp_stream = convert_to_webp(file.file)

        # Save converted WebP to disk
        with open(full_photo_path, "wb") as f:
            f.write(webp_stream.read())
        logger.debug(f"Saved original WebP image to {full_photo_path}")

        # Generate WebP thumbnail from the webp_stream
        webp_stream.seek(0)  # Reset stream for thumbnail generation
        logger.debug("Generating thumbnail")
        thumbnail_stream = generate_thumbnail(webp_stream)

        # Save thumbnail to disk
        with open(thumbnail_photo_path, "wb") as f:
            f.write(thumbnail_stream.read())
        logger.debug(f"Saved thumbnail to {thumbnail_photo_path}")

        # Get the actual file size of the WebP image
        file_size = full_photo_path.stat().st_size
        logger.info(f"Successfully processed image: {webp_filename} (size: {file_size} bytes)")
    except Exception as e:
        logger.error(f"Failed to process image {file.filename}: {e}", exc_info=True)
        # If conversion fails, delete all created files and raise error
        full_photo_path.unlink(missing_ok=True)
        thumbnail_photo_path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail=f"Failed to process image: {e}") from e

    # Generate URLs for the mounted static directories
    original_url = f"/public/picts/{webp_filename}"
    thumbnail_url = f"/public/picts/thumbnails/{webp_filename}"

    photo = await Photo.create(
        filename=webp_filename,
        original_url=original_url,
        thumbnail_url=thumbnail_url,
        file_size=file_size,
    )

    return PhotoResponse(
        id=photo.id,
        filename=photo.filename,
        original_url=photo.original_url,
        thumbnail_url=photo.thumbnail_url,
        file_size=photo.file_size,
        created_at=photo.created_at.isoformat(),
    )


@router.delete("/photos/{photo_id}")
async def delete_photo(photo_id: int) -> dict[str, str]:
    """Delete a photo, its thumbnail, and database record."""
    logger.info(f"Received delete request for photo ID: {photo_id}")
    photo = await Photo.get_or_none(id=photo_id)

    if not photo:
        logger.warning(f"Photo not found for deletion: ID {photo_id}")
        raise HTTPException(status_code=404, detail="Photo not found")

    full_photo_path = settings.upload_dir / photo.filename
    thumbnail_photo_path = settings.upload_dir / "thumbnails" / photo.filename

    if full_photo_path.exists():
        full_photo_path.unlink()
        logger.debug(f"Deleted original photo file: {full_photo_path}")

    if thumbnail_photo_path.exists():
        thumbnail_photo_path.unlink()
        logger.debug(f"Deleted thumbnail file: {thumbnail_photo_path}")

    await photo.delete()
    logger.info(f"Successfully deleted photo: {photo.filename} (ID: {photo_id})")

    return {"message": f"Photo {photo.filename} deleted successfully"}
