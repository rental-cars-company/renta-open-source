from django.conf import settings
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.constants import MINIMUN_AGE_FOR_REGISTER

uz_phone_format_validator = RegexValidator(
    regex=r"^\+998(9[0-1]|9[3-5]|9[7-9]|33|55|77|88)[0-9]{7}$",
    message=_("Неверный номер"),
)


verification_code_validator = RegexValidator(
    r"^\d{" + str(settings.VERIFICATION_CODE_LENGHT) + r"}$",
    message=_("Код имеет некорректный формат"),
)


def validate_positive(value):
    if value <= 0:
        raise serializers.ValidationError(_("Цена должна быть больше нуля."))


def minimum_age_validator(value):
    if value < MINIMUN_AGE_FOR_REGISTER:
        raise serializers.ValidationError(
            _(f"Вам должно быть не меньше {MINIMUN_AGE_FOR_REGISTER} лет")
        )
