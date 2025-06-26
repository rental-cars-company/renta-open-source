from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response

from api.cars.models import Cars, FavoriteCars
from api.cars.serializers import FavoriteCarsSerializer
from api.cars.services import cars_cache


def add_car_to_favorites(user, pk):
    car = get_object_or_404(Cars, pk=pk)
    created = FavoriteCars.objects.get_or_create(user=user, car=car)[1]
    if not created:
        return Response({"error": _("Авто уже в избранном.")})
    cars_cache.clear_car_cache(pk=car.pk)
    return Response({"message": _("Авто добавлено в избранное.")}, status=201)


def remove_car_from_favorites(user, pk):
    car = get_object_or_404(Cars, pk=pk)
    deleted_count = FavoriteCars.objects.filter(user=user, car=car).delete()[0]
    if deleted_count > 0:
        cars_cache.clear_car_cache(pk=car.pk)
        return Response(
            {"detail": _("Авто удалено из избранного.")}, status=204
        )
    return Response({"error": _("Авто не найдено.")}, status=400)


def get_user_favorites(request, view):
    favorites = (
        FavoriteCars.objects.filter(user=request.user)
        .select_related("car")
        .prefetch_related("car__images")
    )
    cars = [fav.car for fav in favorites]

    if view is not None and hasattr(view, "paginate_queryset"):
        page = view.paginate_queryset(cars)
        if page is not None:
            serializer = FavoriteCarsSerializer(
                page, many=True, context={"request": request}
            )
            return view.get_paginated_response(serializer.data)

    serializer = FavoriteCarsSerializer(
        cars, many=True, context={"request": request}
    )
    return Response(serializer.data)
