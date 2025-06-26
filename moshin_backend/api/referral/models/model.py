import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from api.users.models import User
from common.constants import DECIMAL_MAX_DIGITS, DECIMAL_PLACES
from common.models import ModelBase


class ReferralInfo(ModelBase):
    class Meta(ModelBase.Meta):
        abstract = False
        verbose_name = _("реферальная информация")
        verbose_name_plural = _("Реферальная информация")

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь"),
        related_name="referral",
        unique=True,
    )

    own_referral_code = models.UUIDField(
        verbose_name=_("Свой реферальный токен"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    used_referral_code = models.UUIDField(
        verbose_name=_("Использованый реферальный токен"), blank=True, null=True
    )

    balance = models.DecimalField(
        verbose_name=_("Текущий баланс реферальной скидки"),
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
    )

    users_invited = models.IntegerField(
        verbose_name=_("Число приглашенных пользователей"), default=0
    )
