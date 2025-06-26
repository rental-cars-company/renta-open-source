from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from api.bookings.models import Booking
from common.models import ModelBase

User = get_user_model()


class BookingStatusLog(ModelBase):

    class StatusChoices(models.TextChoices):
        PENDING = "pending", _("В ожидании")
        ON_PROCESS = "on_process", _("В процессе")
        ON_DELIVERY = "on_delivery", _("На доставке")
        ACCEPTED = "accepted", _("Принято")
        FINISHED = "finished", _("Завершено")
        CANCELLED = "cancelled", _("Отменено")

    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name="status_logs"
    )
    old_status = models.CharField(max_length=20, choices=StatusChoices.choices)
    new_status = models.CharField(max_length=20, choices=StatusChoices.choices)
    changed_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"#{self.booking.id}: {self.old_status} → {self.new_status} @ {self.changed_at}"

    class Meta:
        verbose_name = _("статус бронирования")
        verbose_name_plural = _("Статусы бронирований")
