from datetime import date

from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


def calculate_age(birth_date):
    today = date.today()
    return (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )


def validate_age_requirement(age, required_age):
    if age < required_age:
        raise ValidationError(
            _(
                f"Ваш возраст ({age}) меньше минимального "
                f"возраста для этой машины ({required_age})."
            )
        )


def validate_age_requirement_register(age, required_age):
    if age < required_age:
        raise ValidationError(
            _(f"Вам должно быть не меньше {required_age} лет")
        )
