from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

from api.users.models import (
    USER_ROLE_ADMIN,
    USER_ROLE_SUPERUSER,
    User,
)

ROLES_TO_LOGIN_WITH_PASSWORD = (USER_ROLE_SUPERUSER, USER_ROLE_ADMIN)


NO_SMS_RENTERS = (
    ("+998958851218", "111111"),
    ("+998958851217", "111111"),
    ("+998958851216", "111111"),
    ("+998998308940", "111111"),
)


def get_token_pair(user: User) -> dict:
    refresh = RefreshToken().for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def get_user_from_refresh_token(refresh: RefreshToken) -> User:
    user_id = refresh.payload.get(api_settings.USER_ID_CLAIM, None)
    if user_id is None:
        raise AuthenticationFailed("Токен некорректен")

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise AuthenticationFailed("Пользователь не найден или удалён")

    if not api_settings.USER_AUTHENTICATION_RULE(user):
        raise AuthenticationFailed("Пользователь деактивирован")

    return user


def check_admin_renter(phone: str, code: str):
    return (phone, code) in NO_SMS_RENTERS
