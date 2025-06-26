from django.db import models
from django.utils.translation import gettext_lazy as _

from api.cars.models import Cars
from api.promo.models import Coupon
from api.users.models import User
from common.constants import (
    DECIMAL_MAX_DIGITS,
    DECIMAL_PLACES,
    DELIVERY_OPTIONS,
    DELIVERY_PRICE,
    PAYMENT_METHOD_CHOICES,
    RETURN_PICKUP_PRICE,
)
from common.models import ModelBase


class Booking(ModelBase):
    class Meta(ModelBase.Meta):
        verbose_name = _("заказ")
        verbose_name_plural = _("Заказы")
        ordering = ["-created_time"]

    class Status(models.TextChoices):
        PENDING = "pending", _("Заказ получен, ожидает подтверждения")
        ON_PROCESS = "on_process", _("Подготовка к передаче")
        ON_DELIVERY = "on_delivery", _("В пути, если выбрана доставка")
        ACCEPTED = "accepted", _("Автомобиль у пользователя")
        FINISHED = "finished", _("Аренда завершена")
        CANCELLED = "cancelled", _("Отменено пользователем или администратором")

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bookings"
    )
    car = models.ForeignKey(Cars, on_delete=models.CASCADE)
    coupon = models.ForeignKey(
        Coupon, null=True, blank=True, on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20, choices=Status.choices, default="pending"
    )

    agreed_to_terms = models.BooleanField(default=False)

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    # Delivery
    delivery_option = models.CharField(
        max_length=20,
        choices=DELIVERY_OPTIONS,
        verbose_name=_("Способ получения"),
    )
    delivery_latitude = models.FloatField(null=True, blank=True)
    delivery_longitude = models.FloatField(null=True, blank=True)
    courier_name = models.CharField(max_length=100, null=True, blank=True)
    courier_phone = models.CharField(max_length=30, null=True, blank=True)

    # Return pickup
    return_pickup_requested = models.BooleanField(
        default=False,
        verbose_name=_("Забрать машину у клиента"),
        help_text=_(
            "Если True — клиент хочет, чтобы мы сами забрали машину по адресу"
        ),
    )
    return_pickup_address = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Адрес возврата машины клиентом"),
    )

    # Новые поля из BRD:
    driver_requested = models.BooleanField(
        default=False, verbose_name=_("Водитель запрошен")
    )
    identity_verified = models.BooleanField(
        default=False, verbose_name=_("Верификация личности")
    )
    admin_notes = models.TextField(
        null=True, blank=True, verbose_name=_("Заметки администратора")
    )

    # price
    days = models.IntegerField()
    daily_price = models.DecimalField(
        decimal_places=DECIMAL_PLACES, max_digits=DECIMAL_MAX_DIGITS
    )
    rental_price = models.DecimalField(
        decimal_places=DECIMAL_PLACES, max_digits=DECIMAL_MAX_DIGITS
    )
    deposit = models.DecimalField(
        max_digits=DECIMAL_MAX_DIGITS, decimal_places=DECIMAL_PLACES, default=0
    )
    delivery_price = models.DecimalField(
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=DELIVERY_PRICE,
    )
    driver_price = models.DecimalField(
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
    )
    return_pickup_price = models.DecimalField(
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=RETURN_PICKUP_PRICE,
        verbose_name=_("Стоимость забора авто с адреса клиента"),
    )
    total_before_discount = models.DecimalField(
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
    )
    total_after_referral = models.DecimalField(
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
    )
    total_price = models.DecimalField(
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
    )
    referral_discount = models.DecimalField(
        max_digits=DECIMAL_MAX_DIGITS, decimal_places=DECIMAL_PLACES, default=0
    )
    promocode_discount = models.DecimalField(
        max_digits=DECIMAL_MAX_DIGITS, decimal_places=DECIMAL_PLACES, default=0
    )

    #
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES,
        null=True,
        blank=True,
        verbose_name=_("Метод оплаты"),
        help_text=_("Выбранный клиентом метод оплаты: карта или наличные"),
    )
    #

    def __str__(self):
        return f"Booking #{self.pk} - {self.user.phone} - {self.car.model}"

    @property
    def rental_summary(self):
        return {
            "days": self.days,
            "daily_price": self.daily_price,
            "rental_price": self.rental_price,
            #
            "deposit": self.deposit,
            "delivery_price": self.delivery_price,
            "driver_price": self.driver_price,
            "return_pickup_price": self.return_pickup_price,
            # total
            "total_before_discount": self.total_before_discount,
            "total_after_referral": self.total_after_referral,
            "total_price": self.total_price,
            # discounts
            "referral_discount": self.referral_discount,
            "promocode_discount": self.promocode_discount,
        }
