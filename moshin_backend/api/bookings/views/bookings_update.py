from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import exceptions, response, views

from api.bookings.serializers import (
    BookingAdminReadSerializer,
    BookingStatusUpdateSerializer,
)
from api.bookings.services import booking_read, booking_service
from common.permissions import AdminOrSuperuserPermission


@extend_schema(tags=("booking",))
@extend_schema(
    request=BookingStatusUpdateSerializer,
    responses={200: BookingStatusUpdateSerializer},
    methods=["PATCH"],
    summary=_("[admin] Обновить статус"),
)
class BookingUpdateView(views.APIView):
    permission_classes = (AdminOrSuperuserPermission,)
    http_method_names = ["patch", "head", "options", "trace"]

    def get_request_serializer(
        self, *args, **kwargs
    ) -> BookingStatusUpdateSerializer:
        return BookingStatusUpdateSerializer(*args, **kwargs)

    def get_response_serializer(
        self, *args, **kwargs
    ) -> BookingAdminReadSerializer:
        return BookingAdminReadSerializer(*args, **kwargs)

    def patch(self, request, pk):
        booking = booking_read.by_pk(pk)

        if booking is None:
            raise exceptions.NotFound([_("Booking не найден")])

        request_serializer = self.get_request_serializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data: dict = request_serializer.validated_data  # type: ignore

        booking_service.change_status(
            booking=booking,
            new_status=validated_data["status"],
            user_to_notify=booking.user,
        )

        return response.Response(
            {
                "detail": "Статус обновлён",
                "status": validated_data["status"],
            }
        )
