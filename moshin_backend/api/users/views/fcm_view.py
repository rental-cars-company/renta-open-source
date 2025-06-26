from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.fcm_serializer import FCMTokenSerializer


@extend_schema(
    request=FCMTokenSerializer,
    responses={200: serializers.Serializer()},
    methods=["POST"],
    description=_("Сохраняет FCM токен пользователя"),
)
@extend_schema(
    responses={200: FCMTokenSerializer},
    methods=["GET"],
    description=_("Возвращает текущий FCM токен пользователя"),
)
class UpdateFCMTokenView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = FCMTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.fcm_token = serializer.validated_data["device_token"]  # type: ignore
        request.user.save()
        return Response({"detail": _("FCM токен сохранён")})

    def get(self, request):
        return Response({"device_token": request.user.fcm_token})
