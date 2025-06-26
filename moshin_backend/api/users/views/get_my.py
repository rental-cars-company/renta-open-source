from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import (
    extend_schema,
)
from rest_framework import permissions, status, views
from rest_framework.request import Request
from rest_framework.response import Response

from api.users.serializers import UserSerializer


@extend_schema(tags=("auth",))
@extend_schema(
    methods=["GET"],
    responses={200: UserSerializer},
    summary=_("Получить собственного пользователя по jwt"),
)
class GetMyUser(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request: Request, *args, **kwargs):
        user = UserSerializer(request.user)
        return Response(user.data, status=status.HTTP_200_OK)
