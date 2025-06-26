from django_filters import rest_framework as filters

from api.promo.models import Coupon


class PromoFilter(filters.FilterSet):
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = Coupon
        fields = ("active",)
