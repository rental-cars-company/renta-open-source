from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _

from api.bookings.models import Booking
from common.models import ModelBase


class Notification(ModelBase):
    class Meta(ModelBase.Meta):
        abstract = False
        verbose_name = _("Оповещение (FCM)")
        verbose_name_plural = _("Оповещения (FCM)")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    booking_status = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=32)
    message = models.CharField(max_length=255)
    payload = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


class Device(ModelBase):
    class Meta(ModelBase.Meta):
        abstract = False
        verbose_name = _("Устройство (FCM)")
        verbose_name_plural = _("Устройства (FCM)")
        unique_together = ("user", "push_token")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    push_token = models.CharField(max_length=255)
    push_enabled = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
