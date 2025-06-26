from typing import Callable, Sequence

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def PinflValidator(value: str):
    if not len(str(value)) == 14:
        raise ValidationError(
            message=_("ПИНФЛ состоит из 14 цифр"), code="limit_value"
        )


def get_passport_pinfl_validators() -> Sequence[Callable]:
    return [
        PinflValidator,
    ]
