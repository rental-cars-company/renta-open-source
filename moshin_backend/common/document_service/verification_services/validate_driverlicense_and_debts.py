import os
import uuid
from pathlib import Path

import requests
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

load_dotenv(BASE_DIR / "dev.env")

VALIDATION_UZ_TOKEN = os.getenv("VALIDATION_UZ_TOKEN")


def send_to_validate_uz_dl_debts(
    pinfl: int, url: str, sender_pinfl: int | None = None
) -> requests.Response:
    headers = {
        "Api-Key": VALIDATION_UZ_TOKEN,
    }

    if sender_pinfl:
        params = {
            "pin": pinfl,
            "transaction_id": str(uuid.uuid4()),
            "sender_pinfl": sender_pinfl,
            "purpose": "validate for debts",
            "consent": "Yes",
        }
    else:
        params = {
            "pRequestID": f"moshin_{uuid.uuid4()}",
            "applicantPinpp": pinfl,
        }

    response = requests.get(url, headers=headers, params=params)
    return response
