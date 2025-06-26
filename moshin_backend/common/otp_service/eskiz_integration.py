import httpx
from django.conf import settings
from django.core.cache import cache

from .exeptions import OtpAuthError

TOKEN_IN_CACHE_TIME: int = 60 * 60 * 24 * 29  # 29 дней
TOKEN_CACHE_KEY: str = "eskiz_token"

ESKIZ_LOGIN_URL = "https://notify.eskiz.uz/api/auth/login"
ESKIZ_SEND_SMS_URL = "https://notify.eskiz.uz/api/message/sms/send"


def cache_eskiz_bearer_token(
    email: str | None = None, password: str | None = None
):
    if email is None:
        email = settings.ESKIZ_EMAIL
    if password is None:
        password = settings.ESKIZ_PASSWORD

    response = httpx.post(
        url=ESKIZ_LOGIN_URL, json={"email": email, "password": password}
    )
    if response.status_code != 200:
        raise OtpAuthError("Eskiz auth failed")

    token = response.json().get("data").get("token")
    cache.set(TOKEN_CACHE_KEY, token, timeout=TOKEN_IN_CACHE_TIME)
    return token


def get_eskiz_bearer_token() -> str:
    token = cache.get(TOKEN_CACHE_KEY)
    if token is None:
        """
        Подстраховка на всякий случай. Обычно этого не должно происходить.
        Celery должен запрашивать токен каждые 29 дней фоном.
        """
        token = cache_eskiz_bearer_token()
    return token


def eskiz_send_code(phone: str, formatted_message: str) -> httpx.Response:
    token = get_eskiz_bearer_token()
    response = httpx.post(
        url=ESKIZ_SEND_SMS_URL,
        json={
            "mobile_phone": phone,
            "message": formatted_message,
            "from": "4546",
            # 'callback_url': None,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    return response
