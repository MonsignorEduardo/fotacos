"""Photo management API routes."""

import uuid
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from fotacos.api.services.images import generate_thumbnail

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
IMGS_DIR = PROJECT_ROOT / "imgs"
THUMBNAILS_DIR = IMGS_DIR / "thumbnails"

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}

router = APIRouter(tags=["photos"])


class PhotoResponse(BaseModel):
    """Response model for a photo."""

    filename: str
    original_url: str
    thumbnail_url: str


class PhotoListResponse(BaseModel):
    """Response model for listing photos."""

    photos: list[PhotoResponse]
    total: int


@router.get("/photos", response_model=PhotoListResponse)
async def list_photos() -> PhotoListResponse:
    """List all photos in the album."""
    photos = []

    if IMGS_DIR.exists():
        for file_path in IMGS_DIR.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in ALLOWED_EXTENSIONS:
                thumbnail_path = THUMBNAILS_DIR / f"thumb_{file_path.name}"
                photos.append(
                    PhotoResponse(
                        filename=file_path.name,
                        original_url=f"/imgs/{file_path.name}",
                        thumbnail_url=f"/imgs/thumbnails/thumb_{file_path.name}"
                        if thumbnail_path.exists()
                        else f"/imgs/{file_path.name}",
                    )
                )

    return PhotoListResponse(photos=photos, total=len(photos))


@router.post("/photos", response_model=PhotoResponse)
async def upload_photo(file: Annotated[UploadFile, File(description="Photo file to upload")]) -> PhotoResponse:
    """Upload a new photo and generate thumbnail."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    # Validate extension
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    # Generate unique filename to avoid collisions
    unique_id = uuid.uuid4().hex[:8]
    original_name = Path(file.filename).stem
    filename = f"{original_name}_{unique_id}{ext}"

    # Save original file
    file_path = IMGS_DIR / filename
    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    # Generate thumbnail
    thumbnail_filename = f"thumb_{filename}"
    thumbnail_path = THUMBNAILS_DIR / thumbnail_filename

    try:
        generate_thumbnail(file_path, thumbnail_path)
    except Exception as e:
        # If thumbnail generation fails, still return success but log error
        print(f"Warning: Failed to generate thumbnail for {filename}: {e}")

    return PhotoResponse(
        filename=filename,
        original_url=f"/imgs/{filename}",
        thumbnail_url=f"/imgs/thumbnails/{thumbnail_filename}" if thumbnail_path.exists() else f"/imgs/{filename}",
    )


@router.delete("/photos/{filename}")
async def delete_photo(filename: str) -> dict[str, str]:
    """Delete a photo and its thumbnail."""
    file_path = IMGS_DIR / filename
    thumbnail_path = THUMBNAILS_DIR / f"thumb_{filename}"

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Photo not found")

    # Validate the file is within IMGS_DIR (prevent path traversal)
    try:
        file_path.resolve().relative_to(IMGS_DIR.resolve())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid filename") from exc

    # Delete original
    file_path.unlink()

    # Delete thumbnail if exists
    if thumbnail_path.exists():
        thumbnail_path.unlink()

    return {"message": f"Photo {filename} deleted successfully"}
