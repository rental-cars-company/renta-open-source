from datetime import datetime
from decimal import Decimal
from typing import Optional

from api.bookings.models import Booking
from api.cars.models import Cars
from api.promo.models import Coupon
from api.promo.services import coupon_service
from api.referral.services import referral_service
from api.users.models import User
from common.constants import (
    DECIMAL_QUANTIZER,
    DELIVERY_OPTION_DELIVERY,
    DELIVERY_PRICE,
    DRIVER_PRICE_PER_DAY,
    RETURN_PICKUP_PRICE,
)

DEPOSIT_STANDART_LE3 = 1_000_000
DEPOSIT_STANDART_GT3 = 2_000_000
DEPOSIT_PREMIUM_LE3 = 1_500_000
DEPOSIT_PREMIUM_GT3 = 3_000_000


def _calculdate_deposit(car_class: str, days: int) -> int:
    if car_class == "standard":
        return DEPOSIT_STANDART_LE3 if days <= 3 else DEPOSIT_STANDART_GT3

    if car_class == "premium":
        return DEPOSIT_PREMIUM_LE3 if days <= 3 else DEPOSIT_PREMIUM_GT3

    return 0


def details_from_serializer_data(
    validated_data: dict, user: User | None = None
) -> dict[str, int | Decimal | dict[str, int | Decimal]]:
    return calculate_total_price(
        start_datetime=validated_data["start_datetime"],
        end_datetime=validated_data["end_datetime"],
        car=validated_data["car"],
        coupon=validated_data.get("coupon", None),
        is_delivery=validated_data["delivery_option"]
        == DELIVERY_OPTION_DELIVERY,
        delivery_price=validated_data.get("delivery_price", DELIVERY_PRICE),
        driver_requested=validated_data.get("driver_requested", False),
        return_pickup_requested=validated_data.get(
            "return_pickup_requested", False
        ),
        return_pickup_price=validated_data.get(
            "return_pickup_price", RETURN_PICKUP_PRICE
        ),
        user=user,
    )


def calculate_total_price(
    start_datetime: datetime,
    end_datetime: datetime,
    car: Cars,
    coupon: Optional[Coupon] = None,
    is_delivery: bool = False,
    delivery_price: int = 0,
    driver_requested: bool = False,
    driver_price_per_day: int = DRIVER_PRICE_PER_DAY,
    return_pickup_requested: bool = False,
    return_pickup_price: int = RETURN_PICKUP_PRICE,
    user: User | None = None,
) -> dict[str, int | Decimal | dict[str, int | Decimal]]:

    days: int = max((end_datetime.date() - start_datetime.date()).days, 1)
    rental_no_discount: Decimal = car.price * days

    driver_price: Decimal = Decimal(
        driver_price_per_day * days if driver_requested else 0
    )

    deposit = (
        Decimal(0)
        if driver_requested
        else Decimal(_calculdate_deposit(car_class=car.car_class, days=days))
    )
    delivery_cost = Decimal(delivery_price if is_delivery else 0)
    return_pickup_cost = Decimal(
        return_pickup_price if return_pickup_requested else 0
    )

    price_no_rental = delivery_cost + driver_price + return_pickup_cost

    # -- NO DISCOUNTS --
    total_no_discount = rental_no_discount + price_no_rental + deposit
    # -- --

    # -- AFTER REFERRAL DISCOUNT --
    if user:
        rental_after_referral, _ = referral_service.referral_discounted_price(
            user, rental_no_discount
        )
        total_after_referral = rental_after_referral + price_no_rental + deposit
        referral_discount = rental_no_discount - rental_after_referral
    else:
        rental_after_referral = rental_no_discount
        total_after_referral = total_no_discount
        referral_discount = Decimal(0)
    # -- --

    # -- AFTER PROMOCODE --
    if coupon:
        rental_price = coupon_service.get_discounted_price(
            rental_after_referral, coupon
        )
        promocode_discount = rental_after_referral - rental_price
    else:
        rental_price = rental_after_referral
        promocode_discount = Decimal(0)
    # -- --

    total = rental_price + price_no_rental + deposit

    return {
        "days": days,
        "daily_price": car.price.quantize(DECIMAL_QUANTIZER),
        "rental_price": rental_no_discount.quantize(DECIMAL_QUANTIZER),
        #
        "deposit": deposit.quantize(DECIMAL_QUANTIZER),
        "delivery_price": delivery_cost.quantize(DECIMAL_QUANTIZER),
        "driver_price": driver_price.quantize(DECIMAL_QUANTIZER),
        "return_pickup_price": return_pickup_cost.quantize(DECIMAL_QUANTIZER),
        # total
        "total_before_discount": total_no_discount.quantize(DECIMAL_QUANTIZER),
        "total_after_referral": total_after_referral.quantize(
            DECIMAL_QUANTIZER
        ),
        "total_price": total.quantize(DECIMAL_QUANTIZER),
        "referral_discount": referral_discount.quantize(DECIMAL_QUANTIZER),
        "promocode_discount": promocode_discount.quantize(DECIMAL_QUANTIZER),
    }


def by_pk(pk) -> Optional[Booking]:
    return Booking.objects.filter(pk=pk).first()
