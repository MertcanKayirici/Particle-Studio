"""Image loading and validation."""

from pathlib import Path
from PIL import Image


SUPPORTED_FORMATS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}


def load_image(path: str | Path) -> Image.Image:
    """Load an image as RGB while preserving the original file."""
    image_path = Path(path)
    if image_path.suffix.lower() not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported image format: {image_path.suffix}")
    with Image.open(image_path) as image:
        return image.convert("RGB")
