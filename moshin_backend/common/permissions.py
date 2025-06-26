from rest_framework.permissions import SAFE_METHODS, BasePermission

from api.users.services import user_read


class IsAdminOrReadOnly(BasePermission):
    """Только админам разрешены изменения (POST, PUT, DELETE).
    Остальные могут только читать (GET и т.п.).
    """

    def has_permission(self, request, view):  # type: ignore
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return user.is_authenticated and user_read.is_admin(user)


class AuthorOrAdmin(BasePermission):
    """Разрешение, позволяющее редактировать объект только автору и админу."""

    def has_object_permission(self, request, view, obj):  # type: ignore
        user = request.user
        return obj.user == user or user_read.is_admin(user)


class OnlyRenterPermission(BasePermission):
    def has_permission(self, request, view):  # type: ignore
        return user_read.is_renter(request.user)


class AdminOrSuperuserPermission(BasePermission):
    def has_permission(self, request, view):  # type: ignore
        return user_read.is_admin(request.user)


class OnlySuperuserPermission(BasePermission):
    def has_permission(self, request, view):  # type: ignore
        return user_read.is_superuser(request.user)
