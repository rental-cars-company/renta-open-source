from typing import Any

from PIL.Image import Image

from .exeptions import ReadingDocumentError


def parse_main_passport_old_data(text: str) -> dict[str, Any]:
    return {}


def get_passport_old_data(image: Image, language="uzb"):
    """Не реализовано."""
    raise ReadingDocumentError()
