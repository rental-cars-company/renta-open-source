import os

from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

ALLOWED_PROFILE_FILE_EXTENSIONS = (".png", ".jpg", ".jpeg")


def profile_photo_extension_validator(value):
    extension = os.path.splitext(value.name)[1]
    if extension not in ALLOWED_PROFILE_FILE_EXTENSIONS:
        raise ValidationError(
            _(
                f"Неверный формат файла. "
                f"Разрешенные форматы: {' '.join(
                    ALLOWED_PROFILE_FILE_EXTENSIONS
                )}"
            )
        )
