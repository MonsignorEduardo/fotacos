"""Image processing service using PIL."""

from io import BytesIO
from typing import BinaryIO

from PIL import ExifTags, Image

from fotacos.env import get_settings

settings = get_settings()
THUMBNAIL_SIZE = (settings.thumbnail_size, settings.thumbnail_size)


def convert_to_webp(
    input_photo: BinaryIO,
    quality: int | None = None,
) -> BinaryIO:
    """
    Convert an image to WebP format.

    Args:
        input_photo: BinaryIO stream containing the source image
        quality: WebP quality (0-100), default 90

    Returns:
        BinaryIO stream containing the converted WebP image
    """
    if quality is None:
        quality = 90  # High quality for original images

    # Reset stream position to beginning
    input_photo.seek(0)

    with Image.open(input_photo) as img:
        # Fix orientation from EXIF data
        img = _fix_orientation(img)

        # Convert to RGB if necessary
        if img.mode in ("RGBA", "P"):
            # For WebP, we can preserve transparency
            if img.mode == "P":
                img = img.convert("RGBA")
        elif img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")

        # Save as WebP to BytesIO
        output = BytesIO()
        img.save(output, "WEBP", quality=quality, method=6)

        # Reset output stream position for reading
        output.seek(0)
        return output


def generate_thumbnail(
    input_photo: BinaryIO,
    size: tuple[int, int] | None = None,
) -> BinaryIO:
    """
    Generate a thumbnail from the source image.

    Args:
        input_photo: BinaryIO stream containing the source image
        size: Thumbnail dimensions (width, height), default from settings

    Returns:
        BinaryIO stream containing the thumbnail WebP image
    """
    if size is None:
        size = THUMBNAIL_SIZE

    # Reset stream position to beginning
    input_photo.seek(0)

    with Image.open(input_photo) as img:
        # Fix orientation from EXIF data
        img = _fix_orientation(img)

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

        # Save as WebP to BytesIO
        output = BytesIO()
        img.save(output, "WEBP", quality=settings.thumbnail_quality, method=6)

        # Reset output stream position for reading
        output.seek(0)
        return output


def _get_exif_orientation(image: Image.Image) -> int | None:
    """Get EXIF orientation value from image."""
    try:
        exif = image.getexif()
        if exif is not None:
            for tag, value in exif.items():
                if ExifTags.TAGS.get(tag) == "Orientation":
                    return value
    except (AttributeError, KeyError, IndexError):
        pass
    return None


def _fix_orientation(image: Image.Image) -> Image.Image:
    """Fix image orientation based on EXIF data."""
    orientation = _get_exif_orientation(image)

    if orientation is None:
        return image

    # Apply transformations based on orientation value
    operations = {
        2: (Image.Transpose.FLIP_LEFT_RIGHT,),
        3: (Image.Transpose.ROTATE_180,),
        4: (Image.Transpose.FLIP_TOP_BOTTOM,),
        5: (Image.Transpose.FLIP_LEFT_RIGHT, Image.Transpose.ROTATE_90),
        6: (Image.Transpose.ROTATE_270,),
        7: (Image.Transpose.FLIP_LEFT_RIGHT, Image.Transpose.ROTATE_270),
        8: (Image.Transpose.ROTATE_90,),
    }

    if orientation in operations:
        for operation in operations[orientation]:
            image = image.transpose(operation)

    return image
