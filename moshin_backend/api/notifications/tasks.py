from celery import shared_task

from api.bookings.models import Booking
from api.notifications.services import NotificationService


@shared_task
def send_pickup_reminder(booking_id):
    b = Booking.objects.filter(pk=booking_id).first()
    if b and b.status in ("pending", "on_process"):
        NotificationService.create(b.user, b, "pickup_reminder", {"ref": b.id})


@shared_task
def send_fuel_return_alert(booking_id):
    b = Booking.objects.filter(pk=booking_id).first()
    if not b:
        return
    fuel = b.initial_fuel_level
    key = (
        "fuel_return_alert_delivery"
        if b.delivery_option == "delivery"
        else "fuel_return_alert"
    )
    NotificationService.create(b.user, b, key, {"fuel_level": fuel})
