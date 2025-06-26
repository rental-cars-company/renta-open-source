from typing import Any

from rest_framework.permissions import IsAuthenticated

from api.users.services import user_read
from common.constants import action as action_t
from common.permissions import AdminOrSuperuserPermission, AuthorOrAdmin


class DocumentPermissionMixin:
    """Permission mixin для документов."""

    action: str

    __RENTER_ALLOWED_ACTIONS = (
        action_t.RETRIEVE,
        action_t.PATCH,
        action_t.DELETE,
    )

    def get(self):
        if self.action in self.__RENTER_ALLOWED_ACTIONS:
            return [IsAuthenticated(), AuthorOrAdmin()]
        return [IsAuthenticated(), AdminOrSuperuserPermission()]


class AdminSerializerMixin:
    """Mixin реализующий логику разных сериализаторов для админов и обычных пользователей.
    В зависимости от роли будет будет выбран один из:
    - admin_serializer_class
    - serializer_class.
    """

    serializer_class: Any
    admin_serializer_class: Any
    request: Any

    def get_serializer_class(self):
        if user_read.is_admin(self.request.user):
            return self.admin_serializer_class
        return self.serializer_class
