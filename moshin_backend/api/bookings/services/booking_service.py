from typing import Optional

from api.bookings.models import Booking
from api.users.models import User
from common.document_service.verification_services.send_to_telegram import (
    send_to_telegram,
)


def create(
    user: User,
    rental_summary: dict,
    validated_serializer_data: dict,
    # do_verify: bool = True,
) -> Booking:
    """Создаём бронирование и запускаем проверку прав, если нужно."""
    # убираем поле доставки, если пришло лишнее
    validated_serializer_data.pop("delivery_price", None)
    booking = Booking(
        user=user,
        **rental_summary,
        **validated_serializer_data,
    )
    booking.save()

    send_to_telegram(f"🎉 Booking {booking.id} создан для user {user.id}")

    # if do_verify:
    #     verify_dl_debts_task.delay(booking.user.id)
    #     send_to_telegram(f"🔍 Запущена verify_dl_debts_task для user {user.id}")

    return booking


def change_status(
    booking: Booking,
    new_status: str,
    user_to_notify: Optional[User] = None,
) -> None:
    """Просто обновляем статус в базе — а дальнейшие уведомления
    и напоминания обрабатываются в signals.py.
    """
    old_status = booking.status
    booking.status = new_status
    booking.save(update_fields=["status"])

    send_to_telegram(
        f"🔄 change_status: booking={booking.id}, {old_status} → {new_status}"
    )

    if user_to_notify is None:
        send_to_telegram(
            "⚠️ user_to_notify=None, уведомления будут отработаны сигналами"
        )
    else:
        send_to_telegram(f"👤 user_to_notify={user_to_notify.id}")
