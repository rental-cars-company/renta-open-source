from typing import Callable, Sequence
from uuid import UUID

from celery import shared_task

from api.driverlicenses.models import DriverLicense
from api.passports.models import Passport
from common.documents.constants import (
    DOCUMENT_EXTRACT_FAILED,
    DOCUMENT_EXTRACT_VERIFIED,
)
from common.documents.services import scan_service
from common.files import (
    get_drivelicense_image_full_path,
    get_passport_image_full_path,
)


@shared_task
def scan_driverlicense(uuid: UUID, image_path: str):
    obj = DriverLicense.objects.filter(pk=uuid)

    try:
        full_path = get_drivelicense_image_full_path(image_path)
        images = scan_service.open_file(full_path)
        data = scan_service.get_driverlicense_data(images[0])

    except scan_service.ReadingDocumentError:
        obj.update(validation_status=DOCUMENT_EXTRACT_FAILED)
        return

    obj.update(validation_status=DOCUMENT_EXTRACT_VERIFIED, **data)


def _scan_password_base(uuid: UUID, scan_func: Callable, scan_args: Sequence):
    obj = Passport.objects.filter(pk=uuid)

    try:
        data = scan_func(*scan_args)

    except scan_service.ReadingDocumentError:
        obj.update(validation_status=DOCUMENT_EXTRACT_FAILED)
        return

    obj.update(verification_status=DOCUMENT_EXTRACT_VERIFIED, **data)


@shared_task
def scan_passport_new(uuid: UUID, image_path_1: str, image_path_2: str):

    full_path_1 = get_passport_image_full_path(image_path_1)
    images = scan_service.open_file(full_path_1)

    if len(images) == 1:
        full_path_2 = get_passport_image_full_path(image_path_2)
        images.append(scan_service.open_file(full_path_2)[0])

    _scan_password_base(
        uuid=uuid,
        scan_func=scan_service.get_passport_new_data,
        scan_args=images,
    )


@shared_task
def scan_passport_old(uuid: UUID, image_path: str):
    full_path = get_drivelicense_image_full_path(image_path)
    images = scan_service.open_file(full_path)

    _scan_password_base(
        uuid=uuid,
        scan_func=scan_service.get_passport_old_data,
        scan_args=(images[0],),
    )
