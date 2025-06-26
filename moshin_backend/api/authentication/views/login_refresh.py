from django.utils.translation import gettext as _
from drf_spectacular.utils import extend_schema
from rest_framework import exceptions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from api.authentication.serializers import (
    LoginResponseSerializer,
    RefreshSerializer,
)
from api.authentication.services import auth_service

from .login_base import LoginViewBase


@extend_schema(tags=("auth",))
@extend_schema(
    request=RefreshSerializer,
    responses={201: LoginResponseSerializer()},
    methods=["POST"],
    summary="Обновить токены",
)
class TokenRefreshView(LoginViewBase):
    def get_request_serializer(self, *args, **kwargs) -> RefreshSerializer:
        return RefreshSerializer(*args, **kwargs)

    def post(self, request: Request, *args, **kwargs) -> Response:
        validated_data = self.get_validated_data(request)


        try:
            refresh = RefreshToken(validated_data["refresh"])
        except TokenError:
            raise exceptions.AuthenticationFailed(
                _("Неверный или просроченный токен")
            )


        try:
            user = auth_service.get_user_from_refresh_token(refresh)
        except exceptions.AuthenticationFailed:
            raise exceptions.AuthenticationFailed(
                _("Неверный или просроченный токен")
            )

        return Response(
            self.get_response_serializer(user).initial_data,
            status=status.HTTP_201_CREATED,
        )