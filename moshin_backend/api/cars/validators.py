import re
from datetime import datetime

from django.utils.translation import gettext_lazy as _

from common.constants import CARS_MIN_YEAR


def validate_year_value(year):
    current = datetime.now().year
    if year > current:
        raise ValueError(_("Год выпуска не может быть в будущем."))
    if year < CARS_MIN_YEAR:
        raise ValueError(
            _(f"Мы не принимаем машины старше {CARS_MIN_YEAR} года.")
        )
    return year


def validate_license_plate_format(plate):
    cleaned = plate.replace(" ", "").upper()
    pattern = r"^(\d{2})([A-Z])(\d{3,4})([A-Z]{2})$"
    match = re.match(pattern, cleaned)
    if not match:
        raise ValueError(_("Номерной знак должен быть в формате: 01 N 951 LA"))

    region, first_letter, digits, last_letters = match.groups()
    return f"{region} {first_letter} {digits} {last_letters}"


def normalize_phone_number(phone):
    digits = re.sub(r"\D", "", phone)

    if digits.startswith("998"):
        formatted = f"+{digits}"
    elif digits.startswith("0") and len(digits) == 9:
        formatted = f"+998{digits[1:]}"
    elif len(digits) == 9:
        formatted = f"+998{digits}"
    else:
        raise ValueError(
            _("Введите номер в формате +998901234567 или 901234567")
        )

    if not re.match(r"^\+998\d{9}$", formatted):
        raise ValueError(
            _("Номер телефона должен быть в формате +998XXXXXXXXX")
        )

    return formatted
