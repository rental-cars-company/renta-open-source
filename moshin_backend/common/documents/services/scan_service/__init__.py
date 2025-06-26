from .driverlicense import get_driverlicense_data
from .exeptions import ReadingDocumentError
from .file_to_pil import open_file
from .passport_new import get_passport_new_data
from .passport_old import get_passport_old_data
from .scaner import init_tesseract

init_tesseract()


__all__ = (
    "get_passport_new_data",
    "get_passport_old_data",
    "get_driverlicense_data",
    "open_file",
    "ReadingDocumentError",
)
