from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters as drf_filters
from rest_framework import viewsets

from api.promo.filter import PromoFilter
from api.promo.models import Coupon
from api.promo.serializers import CouponSerializer
from common.pagination import DynamicPagination
from common.permissions import AdminOrSuperuserPermission


@extend_schema(tags=("promo-codes",))
class CouponViewSet(viewsets.ModelViewSet):
    pagination_class = DynamicPagination
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = (AdminOrSuperuserPermission,)
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter]
    filterset_class = PromoFilter
    search_fields = ["name"]
