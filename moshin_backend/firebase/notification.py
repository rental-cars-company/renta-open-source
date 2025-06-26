import json

import requests
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from google.auth.transport.requests import Request
from google.oauth2 import service_account

# Константы для FCM
PROJECT_ID = settings.FIREBASE_PROJECT_ID
FCM_ENDPOINT = (
    f"https://fcm.googleapis.com/v1/projects/{PROJECT_ID}/messages:send"
)
SCOPES = ["https://www.googleapis.com/auth/firebase.messaging"]
SERVICE_ACCOUNT_FILE = settings.FIREBASE_CREDENTIALS_PATH


def get_access_token():
    """Получение access token для авторизации в Firebase Cloud Messaging."""
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    credentials.refresh(Request())
    return credentials.token


def send_fcm_message(device_token, title, body, data=None):
    """Базовая отправка FCM-сообщения через HTTP v1 API Firebase."""
    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; UTF-8",
    }
    message = {
        "message": {
            "token": device_token,
            "notification": {
                "title": title,
                "body": body,
            },
        }
    }
    if data:
        message["message"]["data"] = {k: str(v) for k, v in data.items()}

    response = requests.post(
        FCM_ENDPOINT, headers=headers, data=json.dumps(message)
    )
    print(_("Статус FCM:"), response.status_code)
    print(_("Ответ FCM:"), response.text)
    return response


def send_fuel_level_reminder(user, fuel_level):
    """Отправка специального уведомления о возврате автомобиля с топливом."""
    if not user.fcm_token:
        print(_("У пользователя нет FCM токена:"), user.id)
        return

    message = _(
        f"Пожалуйста, верните автомобиль с уровнем топлива: {fuel_level} литров."
    )

    send_fcm_message(
        device_token=user.fcm_token,
        title=_("⛽ Напоминание о топливе"),
        body=message,
        data={"fuel_level": str(fuel_level)},
    )
