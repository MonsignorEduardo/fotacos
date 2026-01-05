"""Image processing service using PIL."""

from pathlib import Path

from PIL import ExifTags, Image

# Default thumbnail size
THUMBNAIL_SIZE = (300, 300)


def get_exif_orientation(image: Image.Image) -> int | None:
    """Get EXIF orientation value from image."""
    try:
        exif = image._getexif()
        if exif is not None:
            for tag, value in exif.items():
                if ExifTags.TAGS.get(tag) == "Orientation":
                    return value
    except (AttributeError, KeyError, IndexError):
        pass
    return None


def fix_orientation(image: Image.Image) -> Image.Image:
    """Fix image orientation based on EXIF data."""
    orientation = get_exif_orientation(image)

    if orientation is None:
        return image

    # Apply transformations based on orientation value
    operations = {
        2: (Image.FLIP_LEFT_RIGHT,),
        3: (Image.ROTATE_180,),
        4: (Image.FLIP_TOP_BOTTOM,),
        5: (Image.FLIP_LEFT_RIGHT, Image.ROTATE_90),
        6: (Image.ROTATE_270,),
        7: (Image.FLIP_LEFT_RIGHT, Image.ROTATE_270),
        8: (Image.ROTATE_90,),
    }

    if orientation in operations:
        for operation in operations[orientation]:
            image = image.transpose(operation)

    return image


def generate_thumbnail(
    source_path: Path,
    dest_path: Path,
    size: tuple[int, int] = THUMBNAIL_SIZE,
) -> Path:
    """
    Generate a thumbnail from the source image.

    Args:
        source_path: Path to the source image
        dest_path: Path where thumbnail will be saved
        size: Thumbnail dimensions (width, height), default 300x300

    Returns:
        Path to the generated thumbnail
    """
    # Ensure destination directory exists
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(source_path) as img:
        # Fix orientation from EXIF data
        img = fix_orientation(img)

        # Convert to RGB if necessary (for PNG with transparency, etc.)
        if img.mode in ("RGBA", "P"):
            # Create white background for transparent images
            background = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
            img = background
        elif img.mode != "RGB":
            img = img.convert("RGB")

        # Create thumbnail maintaining aspect ratio
        img.thumbnail(size, Image.Resampling.LANCZOS)

        # Save as JPEG for consistency and smaller file size
        output_path = dest_path.with_suffix(".jpg")
        img.save(output_path, "JPEG", quality=85, optimize=True)

        return output_path
