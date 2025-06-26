from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from api.bookings.models import Booking
from common.models import ModelBase


class Payment(ModelBase):
    class Method(models.TextChoices):
        CARD = 'card', _('Card')
        CASH = 'cash', _('Cash')

    class Status(models.TextChoices):
        INITIATED = "INITIATED", _("Инициализирован")
        PENDING   = "PENDING",   _("Ожидает")
        SUCCESS   = "SUCCESS",   _("Успешно")
        FAILED    = "FAILED",    _("Ошибка")
        CANCELLED = "CANCELLED", _("Отменён")

    class HoldStatus(models.TextChoices):
        NONE       = "NONE",       _("Без холда")
        AUTHORIZED = "AUTHORIZED", _("Авторизован")
        CAPTURED   = "CAPTURED",   _("Списан")
        RELEASED   = "RELEASED",   _("Отменён")

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="payments"
    )
    method = models.CharField(
        max_length=10,
        choices=Method.choices,
        default=Method.CARD,
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.INITIATED,
    )

    # SALE fields
    sale_transaction_id = models.BigIntegerField(null=True, blank=True)
    sale_success_id     = models.BigIntegerField(null=True, blank=True)
    sale_amount         = models.BigIntegerField(null=True, blank=True)

    # HOLD fields
    hold_transaction_id = models.BigIntegerField(null=True, blank=True)
    hold_success_id     = models.BigIntegerField(null=True, blank=True)
    deposit_amount      = models.BigIntegerField(null=True, blank=True)
    hold_status         = models.CharField(
        max_length=10,
        choices=HoldStatus.choices,
        default=HoldStatus.NONE,
    )
    hold_release_date   = models.DateTimeField(null=True, blank=True)

    # Callback
    atm_invoice  = models.CharField(max_length=255, null=True, blank=True)
    request_sign = models.CharField(max_length=255, null=True, blank=True)
    reverse_transaction_id = models.BigIntegerField(null=True, blank=True)
    reverse_response       = models.JSONField(null=True, blank=True)

    # Card Binding fields
    card_transaction_id = models.BigIntegerField(null=True, blank=True)
    card_id             = models.BigIntegerField(null=True, blank=True)
    card_token          = models.CharField(max_length=255, null=True, blank=True)
    pan                 = models.CharField(max_length=20, null=True, blank=True)
    expiry              = models.CharField(max_length=4,  null=True, blank=True)
    card_holder         = models.CharField(max_length=100,null=True, blank=True)
    card_balance        = models.BigIntegerField(null=True, blank=True)
    card_phone          = models.CharField(max_length=20, null=True, blank=True)

    # Business
    keep_deposit = models.BooleanField(default=False)

    def __str__(self):
        return f"Платёж #{self.pk} [{self.method}] – {self.status}"


class Card(models.Model):
    user        = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cards"
    )
    card_id     = models.BigIntegerField()
    card_token  = models.CharField(max_length=255)
    pan         = models.CharField(max_length=20)
    expiry      = models.CharField(max_length=4)
    card_holder = models.CharField(max_length=100, blank=True)
    card_phone  = models.CharField(max_length=20,  blank=True)
    balance     = models.BigIntegerField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "card_id")

    def __str__(self):
        return f"{self.user.username}: ****{self.pan[-4:]}"