from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from api.users.models import User
from common.models import ModelBase


class Deposit(ModelBase):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Пользователь"),
        related_name="deposits",
    )
    deposit = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name=_("Сумма депозита"),
        default=Decimal("0.00"),
    )

    class Meta:
        verbose_name = _("депозит")
        verbose_name_plural = _("Депозиты")

    def __str__(self):
        return f"{self.user} — {self.deposit} UZS"
