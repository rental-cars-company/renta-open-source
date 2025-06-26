from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.notifications.models import Device, Notification
from api.notifications.serializers import (
    DeviceSerializer,
    NotificationSerializer,
)
from api.notifications.services import DeviceService


class NotificationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        qs = Notification.objects.filter(user=self.request.user).select_related(
            "booking__car"
        )
        if self.request.query_params.get("unread") == "true":
            qs = qs.filter(is_read=False)
        return qs


class DeviceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer
    http_method_names = ["post", "get", "delete"]

    def get_queryset(self):
        return Device.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        token = serializer.validated_data["push_token"]
        self.instance = DeviceService.register_or_update_token(
            self.request.user, token
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            self.get_serializer(self.instance).data, status=status.HTTP_200_OK
        )
