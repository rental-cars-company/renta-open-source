from django.db.models import Prefetch
from rest_framework.response import Response

from api.cars.models import CarImage, Cars

from . import cars_cache


def get_all_cars():
    return (
        Cars.objects.select_related("fleet")
        .select_related("fleet__location")
        .prefetch_related(
            Prefetch("images", queryset=CarImage.objects.order_by("order"))
        )
        .all()
    )


def create_car(serializer):
    car = serializer.save()
    cars_cache.clear_car_cache()
    return car


def update_car(serializer):
    car = serializer.save()
    cars_cache.clear_car_cache(pk=car.pk)
    return car


def delete_car(instance):
    cars_cache.clear_car_cache(pk=instance.pk)
    instance.delete()


def get_unique_years(request, view):
    queryset = Cars.objects.only("year").values_list("year", flat=True)
    years = sorted(set(queryset))
    serializer = view.get_serializer({"years": years})
    return Response(serializer.data)


def get_unique_brands(request, view):
    queryset = Cars.objects.only("brand").values_list("brand", flat=True)
    brands = sorted(set(queryset))
    serializer = view.get_serializer({"brands": brands})
    return Response(serializer.data)
