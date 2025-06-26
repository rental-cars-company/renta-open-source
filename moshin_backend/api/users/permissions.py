from rest_framework.permissions import BasePermission

from .models import USER_ROLE_ADMIN, USER_ROLE_SUPERUSER


class UserPermission(BasePermission):

    def has_object_permission(self, request, view, obj):  # type: ignore
        _role = request.user.role

        if obj == request.user:
            return True

        if _role == USER_ROLE_ADMIN and obj.role != USER_ROLE_SUPERUSER:
            return True

        if _role == USER_ROLE_SUPERUSER:
            return True

        return False
