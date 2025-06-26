from typing import TYPE_CHECKING, Optional, Union

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser

from api.users import exeptions
from api.users.models import (
    USER_ROLE_ADMIN,
    USER_ROLE_RENTER,
    USER_ROLE_SUPERUSER,
    User,
)
from common.documents.constants import (
    DOCUMENT_APPROVED,
    DOCUMENT_PENDING,
    DOCUMENT_REJECTED,
)

_T_USER = Union[User, AnonymousUser, AbstractBaseUser]

if TYPE_CHECKING:
    from django.db.models import QuerySet


def verification_status(user) -> str:
    try:
        drive_license_status = user.driverlicense.validation_status
        passport_status = user.passport.validation_status
    except user.__class__.driverlicense.RelatedObjectDoesNotExist:
        return DOCUMENT_PENDING
    except user.__class__.passport.RelatedObjectDoesNotExist:
        return DOCUMENT_PENDING

    if drive_license_status == passport_status == DOCUMENT_APPROVED:
        return DOCUMENT_APPROVED
    if (
        drive_license_status == DOCUMENT_REJECTED
        or passport_status == DOCUMENT_REJECTED
    ):
        return DOCUMENT_REJECTED
    return DOCUMENT_PENDING


def can_rent(user, *, raise_exeption=False) -> bool:
    """Если raise_exeption == True, то будет поднимать исключения.
    UserNoDocuments - нет одного или двух нужных доков.
    UserDocumentsRejected - один или оба документа имеют статус rejected.

    UserWaitsForValidation - документы есть, но админы не проверили еще.
    В этом случае следует оповестить админов о необходимости проверить срочно.
    """
    if raise_exeption is False:
        status = verification_status(user)
        can_rent = status == DOCUMENT_APPROVED
        return can_rent

    try:
        drive_license_status = user.driverlicense.validation_status
        passport_status = user.passport.validation_status

    except user.__class__.driverlicense.RelatedObjectDoesNotExist:
        raise exeptions.UserNoDocuments

    except user.__class__.passport.RelatedObjectDoesNotExist:
        raise exeptions.UserNoDocuments

    if DOCUMENT_REJECTED in (drive_license_status, passport_status):
        raise exeptions.UserDocumentsRejected

    if DOCUMENT_APPROVED == drive_license_status == passport_status:
        return True

    raise exeptions.UserWaitsForValidation


def bookings_count(user: User) -> int:
    return user.bookings.count()  # type: ignore


def by_phone(phone: str) -> Optional[User]:
    return User.objects.filter(phone=phone).first()


def by_username(username: str) -> Optional[User]:
    return User.objects.filter(username=username).first()


def by_credentials(username: str, password: str) -> Optional[User]:
    active_user = User.objects.filter(username=username).first()

    if active_user is None:
        return None

    if not active_user.check_password(password):
        return None

    return active_user


def is_admin(user: User) -> bool:
    return user.role in (USER_ROLE_SUPERUSER, USER_ROLE_ADMIN)


def is_renter(user: User) -> bool:
    return user.role == USER_ROLE_RENTER


def is_superuser(user: User) -> bool:
    return user.role == USER_ROLE_SUPERUSER


def get_queryset() -> "QuerySet":
    return (
        User.objects.select_related("passport", "driverlicense", "referral")
        .prefetch_related("bookings")
        .all()
    )
