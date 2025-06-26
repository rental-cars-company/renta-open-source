from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.bookings.serializers import (
    BookingCreateSerializer,
    BookingReadSerializer,
)
from api.bookings.services import booking_read, booking_service
from api.referral.services import referral_service
from api.referral.services.exeptions import NoReferralError

if TYPE_CHECKING:
    from api.users.models import User


@extend_schema(tags=("booking",))
@extend_schema(
    request=BookingCreateSerializer,
    responses={201: BookingReadSerializer},
    methods=["POST"],
    summary=_("[renter] Забронировать машину"),
)
class BookingCreateView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get_request_serializer(
        self, *args, **kwargs
    ) -> BookingCreateSerializer:
        return BookingCreateSerializer(*args, **kwargs)

    def get_response_serializer(self, *args, **kwargs) -> BookingReadSerializer:
        return BookingReadSerializer(*args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        request_serializer = self.get_request_serializer(
            data=request.data, context={"request": request}
        )
        request_serializer.is_valid(raise_exception=True)
        validated_data: dict = request_serializer.validated_data  # type: ignore
        user: User = request.user

        """Может быть ситуация что у старых юзеров не создан referral.
        Тогда мы считаем для него цену без учета реферальной скидки.
        В дальнейшем можно будет убрать это. Нужно для безопасного перехода.
        """
        try:
            rental_summary = booking_read.details_from_serializer_data(
                validated_data=validated_data, user=user
            )
        except NoReferralError:
            rental_summary = booking_read.details_from_serializer_data(
                validated_data=validated_data,
            )
        # -- --

        booking = booking_service.create(
            user=user,
            rental_summary=rental_summary,
            validated_serializer_data=validated_data,
            #do_verify=True,
        )

        referral_service.referral_set_balance(
            user, user.referral.balance - booking.referral_discount
        )

        return Response(
            self.get_response_serializer(booking).data,
            status=status.HTTP_201_CREATED,
        )
