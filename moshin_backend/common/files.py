from pathlib import Path

from django.conf import settings

from common.constants import DRIVERLICENSES_MEDIA_DIR, PASSPORTS_MEDIA_DIR


def get_drivelicense_image_full_path(name: str) -> str:
    return str(Path(settings.MEDIA_ROOT) / DRIVERLICENSES_MEDIA_DIR / name)


def get_passport_image_full_path(name: str) -> str:
    return str(Path(settings.MEDIA_ROOT) / PASSPORTS_MEDIA_DIR / name)
