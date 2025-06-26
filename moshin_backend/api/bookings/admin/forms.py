from django import forms

from common.constants import (
    DELIVERY_OPTION_DELIVERY,
)

from ..models import Booking
from ..services import booking_read


class BookingAdminForm(forms.ModelForm):

    class Meta:
        model = Booking
        exclude = (
            "rental_price",
            "deposit",
            "delivery_price",
            "driver_price",
            "return_pickup_price",
            "total_before_discount",
            "total_after_referral",
            "total_price",
            "referral_discount",
            "promocode_discount",
            "days",
            "daily_price",
        )

    def save(self, commit: bool = True):
        ins = self.instance
        data = booking_read.calculate_total_price(
            start_datetime=ins.start_datetime,
            end_datetime=ins.end_datetime,
            car=ins.car,
            coupon=ins.coupon,
            is_delivery=ins.delivery_option == DELIVERY_OPTION_DELIVERY,
            delivery_price=ins.delivery_price,
            driver_requested=ins.driver_requested,
            return_pickup_requested=ins.return_pickup_requested,
            user=ins.user,
        )

        ins.rental_price = data["rental_price"]
        ins.deposit = data["deposit"]
        ins.delivery_price = data["delivery_price"]
        ins.driver_price = data["driver_price"]
        ins.return_pickup_price = data["return_pickup_price"]
        ins.total_before_discount = data["total_before_discount"]
        ins.total_after_referral = data["total_after_referral"]
        ins.total_price = data["total_price"]
        ins.referral_discount = data["referral_discount"]
        ins.promocode_discount = data["promocode_discount"]
        ins.days = data["days"]
        ins.daily_price = data["daily_price"]

        return super().save(commit)
