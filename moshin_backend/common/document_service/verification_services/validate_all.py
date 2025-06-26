import os
from pathlib import Path
from typing import Tuple

from dotenv import load_dotenv
from requests import Response

from .send_to_telegram import send_to_telegram
from .validate_driverlicense_and_debts import send_to_validate_uz_dl_debts

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(BASE_DIR / "dev.env")


def validate_dl_debts_criminals(
    pinfl: int,
) -> Tuple[Response, Response, Response | None]:
    """Валидация ВУ, долгов и судимости через validation.uz."""
    urls = {
        "driver": os.getenv("URL_DRIVER_LICENSE"),
        "debts": os.getenv("URL_DEBTS"),
        "criminal": os.getenv("URL_CRIMINAL_RECORDS"),
    }
    sender_pinfl = os.getenv("SENDER_PINFL")

    response_driver = send_to_validate_uz_dl_debts(pinfl, urls["driver"])
    response_debts = send_to_validate_uz_dl_debts(
        pinfl, urls["debts"], sender_pinfl
    )

    # license_data = json.loads(response_driver.text).get("data", {})
    # person = license_data.get("ModelPerson", {})
    # region_id = license_data.get("driverBirthPlace", {}).get("pRegionId")

    response_criminal_records = None
    # response = None
    # if region_id:
    #     birth_date_str = person.get("pOwner_date")
    #     birth_date = (
    #         datetime.strptime(birth_date_str, "%d.%m.%Y")
    #         if birth_date_str
    #         else None
    #     )
    #
    #     if birth_date:
    #         response_criminal_records = send_to_validate_uz_criminal_records(
    #             url=urls["criminal"],
    #             firstname=person.get("pName"),
    #             lastname=person.get("pSurname"),
    #             middlename=person.get("pPatronym"),
    #             birth_year=birth_date.year,
    #             pinfl=pinfl,
    #             passport=person.get("pDoc"),
    #             region_id=region_id,
    #         )

    send_to_telegram(
        f"🛂 Валидация ВУ\nStatus: {response_driver.status_code}\n{response_driver.text}\n\n"
        f"💸 Проверка долгов\nStatus: {response_debts.status_code}\n{response_debts.text}\n\n"
        # f"💸 Проверка судимости\nStatus: {response.status_code}\n{response.text}"
    )

    return response_driver, response_debts, response_criminal_records
