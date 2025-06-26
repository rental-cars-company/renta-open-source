from rest_framework import serializers

from api.promo.models import Coupon


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ("id", "name", "description", "active", "rental_cost_discount")
        read_only_fields = ("id",)
