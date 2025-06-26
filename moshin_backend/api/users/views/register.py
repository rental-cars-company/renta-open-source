from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import exceptions, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.authentication.serializers import CredentialSerializer
from api.users.serializers import UserSerializer
from api.users.services import user_create, user_read
from common.permissions import OnlySuperuserPermission


class RegisterViewBase(views.APIView):

    def get_validated_data(self, request) -> dict:
        serializer = self.get_request_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data: dict = serializer.validated_data  # type: ignore
        return validated_data

    def get_response_serializer(self, user) -> UserSerializer:
        return UserSerializer(user)

    def get_request_serializer(self, *args, **kwargs):
        raise NotImplementedError


@extend_schema(tags=("auth",))
@extend_schema(
    request=CredentialSerializer,
    responses={201: UserSerializer()},
    methods=["POST"],
    summary=_("[Superuser] Создать нового админа"),
)
class CredentialsRegisterView(RegisterViewBase):
    permission_classes = (
        IsAuthenticated,
        OnlySuperuserPermission,
    )

    def get_request_serializer(self, *args, **kwargs) -> CredentialSerializer:
        return CredentialSerializer(*args, **kwargs)

    def get_response_serializer(self, user) -> UserSerializer:
        return UserSerializer(user)

    def post(self, request, *args, **kwargs):
        validated_data: dict = self.get_validated_data(request)

        if user_read.by_username(validated_data["username"]) is not None:
            """Имя пользователя занято"""
            raise exceptions.ValidationError(
                [_("Пользователь с таким логином уже существует")]
            )

        user = user_create.with_credentials(**validated_data)

        return Response(
            self.get_response_serializer(user).data,
            status=status.HTTP_201_CREATED,
        )
