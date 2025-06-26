from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.bookings.serializers import (
    BookingBaseSerializer,
    BookingDetailsSerializer,
)
from api.bookings.services import booking_read
from api.referral.services.exeptions import NoReferralError


@extend_schema(tags=("booking",))
@extend_schema(
    request=BookingBaseSerializer,
    responses={200: BookingDetailsSerializer},
    methods=["POST"],
    summary=_("[renter] Получить детализацию стоимости заказа"),
)
class BookingPriceDetailsView(views.APIView):
    """Рассчитать rental_summary для заказа, не создавая заказ."""

    permission_classes = (IsAuthenticated,)

    def get_request_serializer(self, *args, **kwargs) -> BookingBaseSerializer:
        return BookingBaseSerializer(*args, **kwargs)

    def get_response_serializer(
        self, *args, **kwargs
    ) -> BookingDetailsSerializer:
        return BookingDetailsSerializer(*args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        request_serializer = self.get_request_serializer(
            data=request.data, context={"request": request}
        )
        request_serializer.is_valid(raise_exception=True)

        validated_data: dict = request_serializer.validated_data  # type: ignore

        """Может быть ситуация что у старых юзеров не создан referral.
        Тогда мы считаем для него цену без учета реферальной скидки.
        В дальнейшем можно будет убрать это. Нужно для безопасного перехода.
        """
        try:
            details = booking_read.details_from_serializer_data(
                validated_data, request.user
            )
        except NoReferralError:
            details = booking_read.details_from_serializer_data(validated_data)

        return Response(
            self.get_response_serializer(details).data,
            status=status.HTTP_200_OK,
        )
