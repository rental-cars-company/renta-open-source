import os
from pathlib import Path

import requests
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

load_dotenv(BASE_DIR / "dev.env")

VALIDATION_UZ_TOKEN = os.getenv("VALIDATION_UZ_TOKEN")
ORGANIZATION_ID = os.getenv("ORGANIZATION_ID", 79994)


def send_to_validate_uz_criminal_records(
    url: str,
    firstname: str,
    lastname: str,
    middlename: str,
    birth_year: int,
    pinfl: int,
    passport: str,
    region_id: int,
) -> requests.Response:
    headers = {
        "Api-Key": VALIDATION_UZ_TOKEN,
    }

    params = {
        "firstname": firstname,
        "lastname": lastname,
        "middlename": middlename,
        "birth_year": birth_year,
        "pinfl": pinfl,
        "passport": passport,
        "region_id": region_id,
        "organization_id": 79994,
        "consent": True,
    }

    response = requests.get(url, headers=headers, params=params)
    return response
