from django_filters import rest_framework as filters

from .models import User


class UserFilter(filters.FilterSet):
    role = filters.CharFilter(field_name="role", lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("role",)
