from typing import Any

from PIL.Image import Image

from .exeptions import ReadingDocumentError


def parse_main_passport_new_data(text: str) -> dict[str, Any]:
    return {}


def get_passport_new_data(image1: Image, image2: Image, language="uzb"):
    """Не реализовано."""
    raise ReadingDocumentError()
