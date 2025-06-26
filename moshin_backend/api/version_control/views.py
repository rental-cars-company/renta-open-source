from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)

from .models import AppVersion
from .serializers import AppVersionSerializer


class AppVersionViewSet(viewsets.ModelViewSet):
    queryset = AppVersion.objects.all()
    serializer_class = AppVersionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "patch", "post", "delete"]
