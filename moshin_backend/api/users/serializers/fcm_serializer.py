from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class FCMTokenSerializer(serializers.Serializer):
    device_token = serializers.CharField(
        help_text=_("FCM токен мобильного клиента")
    )
