from typing import Optional

from . import core, exeptions, tasks


def login_send_or_verify(
    phone: str, verification_code: Optional[str], disable=False, app_hash=None
):
    if disable:
        if verification_code is None:
            raise exeptions.CodeSent

        raise exeptions.CodeVerified

    if verification_code is None:
        """
        Если код (verification_code) не был предоствлен.
        Создаем таску на отправку смс-кода на данный номер телефона.
        """
        tasks.send_sms.delay(
            phone,
            core.LOGIN_ACTION,
            {"app_hash": app_hash} if app_hash is not None else {},
        )
        raise exeptions.CodeSent

    if core.verify_sms_code(phone, core.LOGIN_ACTION, verification_code):
        """
        Если код (verification_code) был предоствлен.
        Сверяем код с сохраненным в кеше.
        """
        raise exeptions.CodeVerified

    raise exeptions.WrongCode


def register_send_or_verify(
    phone: str, verification_code: Optional[str], disable=False, app_hash=None
):
    if disable:
        if verification_code is None:
            raise exeptions.CodeSent
        raise exeptions.CodeVerified

    if verification_code is None:
        print(core.cache.get("eskiz_token"))
        tasks.send_sms.delay(
            phone,
            core.REGISTER_ACTION,
            {"app_hash": app_hash} if app_hash is not None else {},
        )
        raise exeptions.CodeSent

    if core.verify_sms_code(phone, core.REGISTER_ACTION, verification_code):
        raise exeptions.CodeVerified

    raise exeptions.WrongCode
