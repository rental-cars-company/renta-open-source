# api/bookings/signals.py
from datetime import timedelta

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import translation

from api.bookings.models import Booking, BookingStatusLog
from api.notifications.services import NotificationService
from api.notifications.tasks import (
    send_fuel_return_alert,
)
from common.document_service.verification_services.send_to_telegram import (
    send_to_telegram,
)


@receiver(pre_save, sender=Booking)
def booking_pre_save(sender, instance: Booking, **kwargs):
    if instance.pk:
        # запомним старый статус
        orig = Booking.objects.filter(pk=instance.pk).first()
        instance._prev_status = orig.status if orig else None


@receiver(post_save, sender=Booking)
def booking_post_save(sender, instance: Booking, created, **kwargs):
    old = getattr(instance, "_prev_status", None)
    new = instance.status
    if old == new:
        send_to_telegram(
            f"ℹ️ Booking {instance.id} saved, но статус не поменялся ({new})."
        )
        return

    send_to_telegram(f"🔄 Booking {instance.id} статус: {old} → {new}")

    try:
        with translation.override(instance.user.language or "ru"):
            translated = BookingStatusLog.StatusChoices(new).label
    except ValueError:
        translated = new
        send_to_telegram(f"⚠️ Неизвестный статус {new}, пушим как есть")

    send_to_telegram(f"🐻 Отправляю NotificationService: {translated}")

    try:
        NotificationService.create(
            user=instance.user,
            booking=instance,
            key=translated,
            ctx={"status": translated},
            payload={"booking_id": str(instance.id)},
        )
    except Exception as e:
        send_to_telegram(f"💥 Ошибка NotificationService: {e}")

    if new == BookingStatusLog.StatusChoices.ACCEPTED:
        send_to_telegram(
            f"⛽ Запускаю send_fuel_return_alert для Booking {instance.id}"
        )
        send_fuel_return_alert.apply_async(
            args=[instance.id], eta=instance.end_datetime - timedelta(hours=1)
        )
