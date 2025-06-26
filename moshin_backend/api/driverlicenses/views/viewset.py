from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets

from api.driverlicenses.models import DriverLicense
from api.driverlicenses.serializers import (
    DriverLicenseAdminSerializer,
    DriverLicenseBaseSerializer,
)
from common.documents.mixins import (
    AdminSerializerMixin,
    DocumentPermissionMixin,
)


@extend_schema(
    tags=("documents",),
    responses=DriverLicenseBaseSerializer,
    request=DriverLicenseBaseSerializer,
)
class DriverLicenseViewSet(
    DocumentPermissionMixin,
    AdminSerializerMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Viewset для водительских прав."""

    queryset = DriverLicense.objects.select_related("user").all()

    http_method_names = ["get", "patch", "delete", "head", "options", "trace"]

    serializer_class = DriverLicenseBaseSerializer
    admin_serializer_class = DriverLicenseAdminSerializer
