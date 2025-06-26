from decimal import Decimal

from api.promo.models import Coupon, UsedCoupon
from api.users.models import User


def get_discounted_price(price: Decimal, coupon: Coupon) -> Decimal:
    mult = Decimal(coupon.rental_cost_discount / 100)
    return price * (1 - mult)


def get_coupon_by_name(name: str) -> Coupon | None:
    return Coupon.objects.filter(name=name).first()


def is_already_used(coupon: Coupon, user: User) -> bool:
    return UsedCoupon.objects.filter(coupon=coupon, user=user).exists()
