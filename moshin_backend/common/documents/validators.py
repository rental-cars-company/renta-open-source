import os

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from common.documents.constants import ALLOWED_DOCUMENT_FILE_EXTENSIONS


def document_file_extension_validator(value):
    extension = os.path.splitext(value.name)[1].lower()
    if extension not in ALLOWED_DOCUMENT_FILE_EXTENSIONS:
        raise ValidationError(
            _(
                f"Неверный формат файла. "
                f"Разрешенные форматы: {' '.join(
                    ALLOWED_DOCUMENT_FILE_EXTENSIONS
                )}"
            )
        )
