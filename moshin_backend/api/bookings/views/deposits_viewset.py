from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from api.bookings.models import Deposit
from api.bookings.serializers import DepositSerializer
from common.permissions import AdminOrSuperuserPermission


@extend_schema(tags=("deposits",))
class DepositViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer
    permission_classes = [AdminOrSuperuserPermission]
