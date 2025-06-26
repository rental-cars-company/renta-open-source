from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets

from api.passports.models import Passport
from api.passports.serializers import (
    PassportAdminSerializer,
    PassportBaseSerializer,
)
from common.documents.mixins import (
    AdminSerializerMixin,
    DocumentPermissionMixin,
)


@extend_schema(
    tags=("documents",),
    responses=PassportBaseSerializer,
    request=PassportBaseSerializer,
)
class PassportViewSet(
    DocumentPermissionMixin,
    AdminSerializerMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Viewset для паспортов."""

    queryset = Passport.objects.select_related("user").all()

    http_method_names = ["get", "patch", "delete", "head", "options", "trace"]

    serializer_class = PassportBaseSerializer
    admin_serializer_class = PassportAdminSerializer
