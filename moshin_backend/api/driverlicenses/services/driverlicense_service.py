from api.driverlicenses.models import DriverLicense
from api.users.models import User
from common.documents.constants import DOCUMENT_PENDING


def get(user_owner: User) -> DriverLicense | None:
    return DriverLicense.objects.filter(user=user_owner).first()


def create_no_scan(
    user_owner: User, image_file, image_file_back
) -> DriverLicense:
    obj = DriverLicense(
        user=user_owner,
        validation_status=DOCUMENT_PENDING,
        image_file=image_file,
        image_file_back=image_file_back,
    )
    obj.save()
    return obj
