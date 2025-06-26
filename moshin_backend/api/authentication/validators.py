from typing import Callable, Sequence

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def VerificationCodeLenghtValidator(value: str):
    if len(str(value)) != settings.VERIFICATION_CODE_LENGHT:
        raise ValidationError(
            message=_(
                f"Код должен состоять из {
                    settings.VERIFICATION_CODE_LENGHT} цифр"
            ),
            code="limit_value",
        )


def get_verification_code_validators() -> Sequence[Callable]:
    return [
        VerificationCodeLenghtValidator,
    ]
