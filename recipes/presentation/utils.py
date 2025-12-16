import tempfile
from pathlib import Path

from PIL import Image, ImageEnhance
from uuid_utils import uuid7


def save_uploaded_file(uploaded_file) -> Path | None:
    # Open image with Pillow
    img: Image.Image = Image.open(uploaded_file)

    # 1. Resize if huge (LLMs struggle with 4k+ resolution sometimes, and it's slow)
    max_size = (1024, 1024)
    img.thumbnail(max_size)

    # 2. Convert to RGB (fixes issues with PNG transparency)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # 3. Enhance Sharpness slightly to help with text/labels
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.5)

    file_path = Path(tempfile.gettempdir()) / f"ingredients_{uuid7().hex}.jpg"
    img.save(file_path, quality=95)

    return Path(file_path)
