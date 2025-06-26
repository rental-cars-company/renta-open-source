from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters as drf_filters
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

# from rest_framework.response import Response
# from rest_framework.decorators import action
from api.users.filter import UserFilter
from api.users.permissions import UserPermission
from api.users.serializers import UserSerializer
from api.users.services import user_read
from common.constants import action
from common.pagination import DynamicPagination
from common.permissions import AdminOrSuperuserPermission


@extend_schema(tags=("users",))
class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):

    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, drf_filters.SearchFilter)
    filterset_class = UserFilter
    pagination_class = DynamicPagination

    search_fields = (
        "username",
        "phone",
    )

    http_method_names = [
        "get",
        "post",
        "patch",
        "delete",
        "head",
        "options",
        "trace",
    ]

    def get_queryset(self):  # type: ignore
        return user_read.get_queryset()

    def get_permissions(self):
        if self.action == action.CREATE:
            return []

        if self.action in (action.DELETE, action.PATCH, action.RETRIEVE):
            return [IsAuthenticated(), UserPermission()]

        return [IsAuthenticated(), AdminOrSuperuserPermission()]
