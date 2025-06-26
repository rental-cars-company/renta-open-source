from celery import shared_task

from . import core


@shared_task
def send_sms(phone: str, action: core._T_Action, format_data: dict):
    return core.send_sms_code(phone, action, format_data)


@shared_task
def cache_otp_api_key():
    core.cache_api_key()
