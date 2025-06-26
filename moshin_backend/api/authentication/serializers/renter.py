from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.validators import (
    uz_phone_format_validator,
    verification_code_validator,
)


class PhoneAndCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(
        write_only=True,
        validators=(uz_phone_format_validator,),
    )
    verification_code = serializers.CharField(
        required=False,
        write_only=True,
        validators=(verification_code_validator,),
        help_text=_("Опционально. Код верификации из смс"),
    )
    app_hash = serializers.CharField(
        required=False,
        write_only=True,
        help_text=_("Для android. Хэш приложения"),
    )
    # TEMP_disable_eskiz = serializers.BooleanField(default=False, initial=False)


class UserRegisterSerializer(PhoneAndCodeSerializer):
    # name = serializers.CharField(
    #     validators=(
    #         RegexValidator(
    #             "([A-Z][a-z]*)|([А-Я][а-я]*)",
    #             message=_(
    #                 "Имя должно быть написано с большой буквы и "
    #                 "не должно содержать специальных символов и цифр"
    #             ),
    #         ),
    #     )
    # )
    # surname = serializers.CharField(
    #     validators=(
    #         RegexValidator(
    #             "([A-Z][a-z]*)|([А-Я][а-я]*)",
    #             message=_(
    #                 "Фамилия должна быть написана с большой буквы и "
    #                 "не должна содержать специальных символов и цифр"
    #             ),
    #         ),
    #     )
    # )
    # age = serializers.IntegerField(validators=User.age.field.validators)

    referral_code = serializers.CharField(required=False, write_only=True)
