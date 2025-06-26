# users/models/__init__.py
from .roles import (
    USER_ROLE_ADMIN,
    USER_ROLE_CHOICES,
    USER_ROLE_RENTER,
    USER_ROLE_SUPERUSER,
)
from .user import User

__all__ = (
    "User",
    "USER_ROLE_ADMIN",
    "USER_ROLE_CHOICES",
    "USER_ROLE_RENTER",
    "USER_ROLE_SUPERUSER",
)


class DriverLicense:
    pass
