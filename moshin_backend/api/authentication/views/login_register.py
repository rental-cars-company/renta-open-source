from django.utils.translation import gettext as _
from drf_spectacular.utils import extend_schema
from rest_framework import exceptions, status
from rest_framework.request import Request
from rest_framework.response import Response

from api.authentication.serializers import (
    LoginResponseSerializer,
    UserRegisterSerializer,
)
from api.authentication.services import auth_service
from api.referral.services import referral_service
from api.users.services import user_create, user_read
from common import otp_service

from .login_base import LoginViewBase


@extend_schema(tags=("auth",))
@extend_schema(
    request=UserRegisterSerializer,
    responses={201: LoginResponseSerializer()},
    methods=["POST"],
    summary="Регистрация + вход",
)
class RenterLoginRegisterView(LoginViewBase):
    def get_request_serializer(self, *args, **kwargs):
        return UserRegisterSerializer(*args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        validated_data = self.get_validated_data(request)
        phone = validated_data["phone"]
        referral_code = validated_data.pop("referral_code", None)

        try:
            #  Валидируем или отправляем смс код
            otp_data = {
                "phone": phone,
                "verification_code": validated_data.pop(
                    "verification_code", None
                ),
                "disable": validated_data.pop("TEMP_disable_eskiz", False),
                "app_hash": validated_data.pop("app_hash", None),
            }

            # TEST ADMIN USER. NO OTP
            if auth_service.check_admin_renter(
                otp_data["phone"], otp_data["verification_code"]
            ):
                if (user := user_read.by_phone(phone)) is None:
                    user = user_create.renter(**validated_data)
                    referral_service.register(user, referral_code)

                return Response(
                    self.get_response_serializer(user).initial_data,
                    status=status.HTTP_201_CREATED,
                )
            # -----

            if user_read.by_phone(phone) is None:
                #  Если такой номер не зарегестрирован, то регаем
                otp_service.register_send_or_verify(**otp_data)
            else:
                #  Если номер зарегестрирован, то логиним
                otp_service.login_send_or_verify(**otp_data)

        except otp_service.CodeSent:
            #  Код отправлен успешно
            return Response(
                {"message": _("Смс код был выслан на Ваш номер телефона")},
                status=status.HTTP_200_OK,
            )

        except otp_service.WrongCode:
            #  Код неверный
            raise exceptions.NotAuthenticated([_("Неверный код")])

        except otp_service.CodeVerified:
            #  Код верный -> регистрируем -> создаем jwt
            if (user := user_read.by_phone(phone)) is None:
                user = user_create.renter(**validated_data)
                referral_service.register(user, referral_code)

            return Response(
                self.get_response_serializer(user).initial_data,
                status=status.HTTP_201_CREATED,
            )
