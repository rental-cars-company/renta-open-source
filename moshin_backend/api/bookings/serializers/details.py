from rest_framework import serializers

from common.constants import DECIMAL_MAX_DIGITS, DECIMAL_PLACES


class BookingDetailsSerializer(serializers.Serializer):
    days = serializers.IntegerField()
    daily_price = serializers.DecimalField(
        decimal_places=DECIMAL_PLACES, max_digits=DECIMAL_MAX_DIGITS
    )
    rental_price = serializers.DecimalField(
        decimal_places=DECIMAL_PLACES, max_digits=DECIMAL_MAX_DIGITS
    )
    deposit = serializers.DecimalField(
        decimal_places=DECIMAL_PLACES, max_digits=DECIMAL_MAX_DIGITS
    )
    delivery_price = serializers.DecimalField(
        decimal_places=DECIMAL_PLACES, max_digits=DECIMAL_MAX_DIGITS
    )
    driver_price = serializers.DecimalField(
        decimal_places=DECIMAL_PLACES, max_digits=DECIMAL_MAX_DIGITS
    )
    return_pickup_price = serializers.DecimalField(
        decimal_places=DECIMAL_PLACES, max_digits=DECIMAL_MAX_DIGITS
    )

    total_before_discount = serializers.DecimalField(
        decimal_places=DECIMAL_PLACES, max_digits=DECIMAL_MAX_DIGITS
    )
    total_after_referral = serializers.DecimalField(
        decimal_places=DECIMAL_PLACES, max_digits=DECIMAL_MAX_DIGITS
    )
    total_price = serializers.DecimalField(
        decimal_places=DECIMAL_PLACES, max_digits=DECIMAL_MAX_DIGITS
    )
    referral_discount = serializers.DecimalField(
        decimal_places=DECIMAL_PLACES, max_digits=DECIMAL_MAX_DIGITS
    )
    promocode_discount = serializers.DecimalField(
        decimal_places=DECIMAL_PLACES, max_digits=DECIMAL_MAX_DIGITS
    )
