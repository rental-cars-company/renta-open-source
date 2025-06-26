from django_filters import rest_framework as filters

from api.bookings.models import Booking
from api.cars.models import Cars


class CarsFilter(filters.FilterSet):
    brand = filters.CharFilter(field_name="brand", lookup_expr="icontains")
    car_class = filters.CharFilter(
        field_name="car_class", lookup_expr="icontains"
    )
    year = filters.NumberFilter(field_name="year")
    price_min = filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Cars
        fields = (
            "brand",
            "car_class",
            "year",
            "price_min",
            "price_max",
        )


class BookingFilter(filters.FilterSet):
    status = filters.CharFilter(field_name="status", lookup_expr="icontains")
    date = filters.DateFilter(field_name="created_time", lookup_expr="date")
    user = filters.CharFilter(field_name="user__id", lookup_expr="exact")
    car = filters.CharFilter(field_name="car__id", lookup_expr="exact")
    fleet = filters.CharFilter(
        field_name="car__fleet__name", lookup_expr="icontains"
    )

    class Meta:
        model = Booking
        fields = [
            "status",
            "date",
            "user",
            "car",
            "fleet",
        ]
