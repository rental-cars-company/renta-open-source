from random import randint
from typing import NewType

from django.conf import settings
from django.core.cache import cache

from .eskiz_integration import cache_eskiz_bearer_token, eskiz_send_code
from .exeptions import FailedCodeSending

SMS_CODE_LIFETIME: int = 60 * 60 * 5  # 5 минут


_T_Message = NewType("_T_Message", str)
REGISTER_MESSAGE = _T_Message(
    "Renta mobil ilovasidan ro'yhatdan o'tish uchun tasdiqlash kodi: {code1}\n\n"
    "Код подтверждения для регистрации в приложении Renta: {code2}"
)
LOGIN_MESSAGE = _T_Message(
    "Renta mobil ilovasiga kirish tasdiqlash kodi: {code1}\n\n"
    "Код подтверждения для входа в приложение Renta: {code2}"
)
REGISTER_MESSAGE_WITH_HASH = _T_Message(
    "Renta mobil ilovasidan ro'yhatdan o'tish uchun tasdiqlash kodi: {code1}\n\n"
    "Код подтверждения для регистрации в приложении Renta: {code2}\n"
    "app: {app_hash}"
)
LOGIN_MESSAGE_WITH_HASH = _T_Message(
    "Renta mobil ilovasiga kirish tasdiqlash kodi: {code1}\n\n"
    "Код подтверждения для входа в приложение Renta: {code2}\n"
    "app: {app_hash}"
)

_T_Action = NewType("_T_Action", str)
LOGIN_ACTION = _T_Action("L")
REGISTER_ACTION = _T_Action("R")


def cache_api_key():
    cache_eskiz_bearer_token()


def verify_sms_code(phone: str, action: _T_Action, code: str) -> bool:
    key = __generate_cache_key(phone, action)
    return cache.get(key) == code


def send_sms_code(phone: str, action: _T_Action, format_data: dict) -> str:
    code = __generate_code_string()
    format_data = {"code1": code, "code2": code, **format_data}

    if action == LOGIN_ACTION:
        if "app_hash" in format_data.keys():
            formatted_message = LOGIN_MESSAGE_WITH_HASH.format(**format_data)
        else:
            formatted_message = LOGIN_MESSAGE.format(**format_data)

    elif action == REGISTER_ACTION:
        if "app_hash" in format_data.keys():
            formatted_message = REGISTER_MESSAGE_WITH_HASH.format(**format_data)
        else:
            formatted_message = REGISTER_MESSAGE.format(**format_data)

    else:
        return "error: wrong_action"

    response = eskiz_send_code(phone, formatted_message)

    if response.status_code != 200:
        print(response.status_code, response.json())
        raise FailedCodeSending(
            f"code: {response.status_code} \n json: {response.json()}"
        )

    cache.set(
        key=__generate_cache_key(phone, action),
        value=code,
        timeout=SMS_CODE_LIFETIME,
    )
    return f"code: {code}"


def __generate_cache_key(phone: str, action: _T_Action):
    return f"sms_{action}_{phone}"


def __generate_code_string() -> str:
    code_lenght: int = settings.VERIFICATION_CODE_LENGHT
    lower_border = int("1" + "0" * (code_lenght - 1))
    upper_border = int("9" * code_lenght)
    return str(randint(lower_border, upper_border))
