from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import exceptions, status, views
from rest_framework.request import Request
from rest_framework.response import Response

from api.users.services import user_read


@extend_schema(tags=("auth",))
@extend_schema(
    methods=["GET"],
    responses={200: OpenApiResponse(description="exists")},
    summary=_("Существует ли renter с данным номером телефона"),
    parameters=[OpenApiParameter("phone", str, required=True)],
)
class CheckPhoneRegisterdView(views.APIView):

    def get(self, request: Request, *args, **kwargs):
        phone = request.query_params.get("phone", None)

        if phone is None:
            raise exceptions.ParseError([_("Необходим параметр phone")])

        if user_read.by_phone(phone=phone) is None:
            return Response({"exists": False}, status=status.HTTP_200_OK)

        return Response({"exists": True}, status=status.HTTP_200_OK)
