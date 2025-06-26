from django.db import models
from django.utils.translation import gettext_lazy as _

from api.promo.models import Coupon
from api.users.models import User
from common.models import ModelBase


class UsedCoupon(ModelBase):
    class Meta(ModelBase.Meta):
        abstract = False
        constraints = [
            models.UniqueConstraint(
                fields=["user", "coupon"], name="unique_used_coupon"
            )
        ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="used_coupons"
    )
    coupon = models.ForeignKey(
        Coupon, on_delete=models.CASCADE, related_name="used_coupons"
    )

    def __str__(self):
        return f'{_("Купон")} {self.coupon} {_("использованный")} {self.user}'
