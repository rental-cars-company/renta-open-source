import os

import requests


def send_to_telegram(text: str) -> None:
    try:
        telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        telegram_url = (
            f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        )

        resp = requests.post(
            telegram_url, data={"chat_id": chat_id, "text": text}
        )
        if resp.status_code != 200:
            print("❌ Ошибка Telegram:", resp.status_code, resp.text)
    except Exception as e:
        print("❗ Ошибка при отправке в Telegram:", e)
