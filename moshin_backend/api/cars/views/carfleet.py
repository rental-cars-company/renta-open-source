from rest_framework import viewsets

from api.cars.models import CarFleet
from api.cars.serializers import CarFleetSerializer
from common.permissions import IsAdminOrReadOnly


class CarFleetViewSet(viewsets.ModelViewSet):
    queryset = CarFleet.objects.all()
    serializer_class = CarFleetSerializer
    filterset_fields = ["id", "name", "owner_phone_number"]
    permission_classes = (IsAdminOrReadOnly,)
