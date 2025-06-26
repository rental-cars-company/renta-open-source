from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import exceptions, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.promo.serializers import CouponSerializer
from api.promo.services import coupon_service


@extend_schema(tags=("promo-codes",))
@extend_schema(
    responses={200: CouponSerializer()},
    methods=["GET"],
    summary="[renter] Получить промокод по его имени",
    parameters=[OpenApiParameter("name", str, required=True)],
    description="Вернет промомкод только если он активен"
    " и не был использован рентером, который отправил запрос",
)
class GetCouponIdByNameView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get_response_serializer(self, *args, **kwargs):
        return CouponSerializer(*args, **kwargs)

    def get(self, request: Request, *args, **kwargs):
        coupon_name = request.query_params.get("name", None)
        if coupon_name:
            coupon_name = coupon_name.upper()

        if coupon_name is None:
            raise exceptions.ParseError([_("Необходим параметр name")])

        coupon = coupon_service.get_coupon_by_name(coupon_name)

        if coupon is None:
            raise exceptions.NotFound([_("Промокод не найден")])

        if not coupon.active:
            raise exceptions.PermissionDenied([_("Промокод больше не активен")])

        if coupon_service.is_already_used(coupon, request.user):
            raise exceptions.NotFound([_("Вы уже использовали этот промокод")])

        serializer = self.get_response_serializer(coupon)
        return Response(serializer.data, status=status.HTTP_200_OK)
