from django.utils.translation import gettext as _
from drf_spectacular.utils import extend_schema
from rest_framework import exceptions, parsers, permissions, status, views
from rest_framework.response import Response

from api.driverlicenses.serializers import DriverLicenseBaseSerializer
from api.driverlicenses.services import driverlicense_service
from common.documents import tasks
from common.documents.serializers import DocumentTwoImageRequestSerializer


@extend_schema(
    request=DocumentTwoImageRequestSerializer,
    responses=DriverLicenseBaseSerializer(),
    tags=("documents",),
    summary="[renter] Загрузить водительские права",
    description="На вход принимает либо две фотографии (.jpg .png) в два поля. "
    "Либо один файл .pdf с двумя страницами",
)
class DriverLicenseCreateView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.MultiPartParser,)

    def get_request_serializer(self, *args, **kwargs):
        return DocumentTwoImageRequestSerializer(*args, **kwargs)

    def get_response_serializer(self, *args, **kwargs):
        return DriverLicenseBaseSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        in_serializer = self.get_request_serializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        validated_data: dict = in_serializer.validated_data  # type: ignore
        user = request.user

        if driverlicense_service.get(user_owner=user) is not None:
            raise exceptions.PermissionDenied([_("У вас уже есть документ")])

        obj = driverlicense_service.create_no_scan(
            user_owner=request.user,
            image_file=validated_data["image_file"],
            image_file_back=validated_data["image_file_back"],
        )

        tasks.scan_driverlicense.delay(
            obj.pk,
            validated_data["image_file"].name,
        )

        out_serializer = self.get_response_serializer(obj)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)
