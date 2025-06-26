from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.bookings.models import Booking
from api.bookings.serializers import (
    BookingAdminReadSerializer,
    BookingReadSerializer,
)
from common.filter import BookingFilter
from common.permissions import AdminOrSuperuserPermission, AuthorOrAdmin
from common.pagination import DynamicPagination


@extend_schema(tags=("booking",))
class BookingReadViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = (
        Booking.objects.select_related("user", "car", "coupon")
        .prefetch_related("user__bookings")
        .select_related(
            "user__passport",
            "user__driverlicense",
        )
        .prefetch_related(
            "car__images",
        )
        .select_related("car__fleet", "car__fleet__location")
        .all()
    )

    serializer_class = BookingReadSerializer
    permission_classes = [AuthorOrAdmin]

    filter_backends = [DjangoFilterBackend]
    filterset_class = BookingFilter
    pagination_class = DynamicPagination

    http_method_names = ["get", "head", "options", "trace"]

    def get_serializer_class(self):
        if self.action in ["admin_all", "admin_get"]:
            return BookingAdminReadSerializer
        return super().get_serializer_class()

    @extend_schema(
        summary="[admin] Получить по айди вместе с скрытой информацией (validate.uz)"
    )
    @action(
        detail=True,
        methods=["GET"],
        permission_classes=[AdminOrSuperuserPermission],
        serializer_class=BookingAdminReadSerializer,
    )
    def admin_get(self, request, pk):
        return super().retrieve(request, pk)

    @extend_schema(summary="[admin] Получить список всех bookings")
    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[AdminOrSuperuserPermission],
        serializer_class=BookingAdminReadSerializer,
    )
    def admin_all(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(summary="[renter] Моя история заказов")
    @action(detail=False, methods=["GET"])
    def history(self, request):
        bookings = self.get_queryset().filter(user=request.user)

        page = self.paginate_queryset(bookings)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)