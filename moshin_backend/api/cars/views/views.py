from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as drf_filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from api.cars.serializers import (
    BrandsSerializer,
    CarsSerializer,
    YearsSerializer,
)
from api.cars.services import cars_cache, cars_service, favorites_service
from common.filter import CarsFilter
from common.pagination import CarsPagination, DynamicPagination
from common.permissions import AuthorOrAdmin, IsAdminOrReadOnly


class CarsViewSet(viewsets.ModelViewSet):
    serializer_class = CarsSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter]
    filterset_class = CarsFilter
    search_fields = ["brand", "model"]
    pagination_class = CarsPagination
    queryset = cars_service.get_all_cars()

    def list_original(self, request):
        return super().list(request)

    def retrieve_original(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        base_cache_key = f"cars:list:{request.get_full_path()}"
        return cars_cache.get_cached_list_response(
            self, request, base_cache_key
        )

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        return cars_cache.get_cached_detail_response(self, request, pk)

    def perform_create(self, serializer):
        return cars_service.create_car(serializer)

    def perform_update(self, serializer):
        return cars_service.update_car(serializer)

    def perform_destroy(self, instance):
        return cars_service.delete_car(instance)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        url_path="favorite",
    )
    def add_to_favorites(self, request, pk=None):
        return favorites_service.add_car_to_favorites(request.user, pk)

    @add_to_favorites.mapping.delete
    def remove_from_favorites(self, request, pk=None):
        return favorites_service.remove_car_from_favorites(request.user, pk)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[AuthorOrAdmin],
        url_path="favorites",
        pagination_class=DynamicPagination,
    )
    def get_favorite_cars(self, request):
        return favorites_service.get_user_favorites(request, view=self)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAdminOrReadOnly],
        serializer_class=YearsSerializer,
        url_path="years",
    )
    def get_only_years(self, request):
        return cars_service.get_unique_years(request, self)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAdminOrReadOnly],
        serializer_class=BrandsSerializer,
        url_path="brands",
    )
    def get_only_brands(self, request):
        return cars_service.get_unique_brands(request, self)
