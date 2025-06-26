from django.utils.translation import gettext as _
from drf_spectacular.utils import extend_schema
from rest_framework import exceptions, status
from rest_framework.request import Request
from rest_framework.response import Response

from api.authentication.serializers import (
    CredentialSerializer,
    LoginResponseSerializer,
    PhoneAndCodeSerializer,
)
from api.users.services import user_read
from common import otp_service

from .login_base import LoginViewBase


@extend_schema(tags=("auth",))
@extend_schema(
    request=PhoneAndCodeSerializer,
    responses={201: LoginResponseSerializer()},
    methods=["POST"],
    summary="[renter] Вход в аккаунт",
)
class LoginWithPhoneView(LoginViewBase):
    def get_request_serializer(self, *args, **kwargs):
        return PhoneAndCodeSerializer(*args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        validated_data = self.get_validated_data(request)
        phone = validated_data["phone"]
        user = user_read.by_phone(phone)

        if user is None:
            raise exceptions.AuthenticationFailed(
                detail=[_("Неверный номер телефона или код подтверждения")],
                code=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            otp_service.login_send_or_verify(
                phone=phone,
                verification_code=validated_data.pop("verification_code", None),
                disable=validated_data.pop("TEMP_disable_eskiz", False),
            )
        except otp_service.CodeSent:
            return Response(
                {"message": _("Смс код был выслан на Ваш номер телефона")},
                status=status.HTTP_200_OK,
            )
        except otp_service.WrongCode:
            raise exceptions.NotAuthenticated([_("Неверный код")])

        except otp_service.CodeVerified:
            return Response(
                self.get_response_serializer(user).initial_data,
                status=status.HTTP_201_CREATED,
            )


@extend_schema(tags=("auth",))
@extend_schema(
    request=CredentialSerializer,
    responses={201: LoginResponseSerializer()},
    methods=["POST"],
    summary="[admin] Вход в аккаунт",
)
class LoginWithCredentialsView(LoginViewBase):
    def get_request_serializer(self, *args, **kwargs):
        return CredentialSerializer(*args, **kwargs)

    def post(self, request: Request, *args, **kwargs) -> Response:
        validated_data = self.get_validated_data(request)

        user = user_read.by_credentials(
            username=validated_data["username"],
            password=validated_data["password"],
        )

        if not user:
            raise exceptions.AuthenticationFailed(
                detail=[_("Неверное имя пользователя или пароль")],
                code=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(
            self.get_response_serializer(user).initial_data,
            status=status.HTTP_201_CREATED,
        )
