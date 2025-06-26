from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import translation
from django.utils.translation import gettext as _
from firebase.notification import send_fcm_message

from api.notifications.models import Device, Notification


class NotificationService:
    @staticmethod
    def _render(user, key, ctx):
        lang = getattr(user, "language", "uz")
        with translation.override(lang):
            return _(key) % ctx

    @classmethod
    def create(cls, user, booking, key, ctx=None, payload=None):
        ctx = ctx or {}
        message = cls._render(user, key, ctx)
        notif = Notification.objects.create(
            user=user,
            booking=booking,
            type=key,
            message=message,
            payload=payload or {},
            booking_status=booking.status,
        )
        cls.dispatch(user, notif)
        return notif

    @staticmethod
    def dispatch(user, notif):
        data = {
            "id": notif.id,
            "message": notif.message,
            "payload": notif.payload,
        }
        layer = get_channel_layer()
        for device in Device.objects.filter(user=user):
            if device.push_enabled:
                # стандартный пуш
                send_fcm_message(
                    device.push_token, notif.message, notif.message, data
                )
            else:
                # in-app через WS
                async_to_sync(layer.group_send)(
                    f"user_{user.id}", {"type": "notification", "data": data}
                )


class DeviceService:
    @staticmethod
    def register_or_update_token(user, token):
        device, created = Device.objects.get_or_create(
            user=user,
            push_token=token,
            defaults={"push_enabled": True},
        )
        if not created:
            device.push_enabled = True
            device.save(update_fields=["push_enabled", "updated_at"])
        return device
