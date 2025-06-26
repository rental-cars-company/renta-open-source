from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import ModelBase


class Coupon(ModelBase):
    class Meta(ModelBase.Meta):
        abstract = False
        verbose_name = _("промокод")
        verbose_name_plural = _("Промокоды")

    name = models.CharField(verbose_name=_("Промокод"), unique=True)
    description = models.CharField(
        verbose_name=_("Описание"),
    )

    active = models.BooleanField(verbose_name=_("Активен"), default=True)

    rental_cost_discount = models.IntegerField(
        verbose_name=_("% Скидки"),
        help_text=_("Скидка только на аренду в процентах"),
        default=0,
    )

    def __str__(self) -> str:
        return f"{self.name}"
