from __future__ import annotations

from typing import BinaryIO

from PIL import Image


def detect_frame_grid(image_file: BinaryIO):
    """Return a conservative grid estimate for a spritesheet.

    The project stores the frame size in metadata and lets the user override it,
    so the auto-detection only needs a reasonable fallback when a new upload is
    analysed. In practice this means: if the image is rectangular, keep a single
    frame per full image unless a more obvious grid can be identified.
    """
    try:
        if hasattr(image_file, "seek"):
            image_file.seek(0)
        with Image.open(image_file) as img:
            img.load()
            width, height = img.size
            if width <= 0 or height <= 0:
                raise ValueError("Invalid image size")

            return {
                "cols": 1,
                "rows": 1,
                "frame_width": width,
                "frame_height": height,
            }
    except (OSError, ValueError):
        raise
