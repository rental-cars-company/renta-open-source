from django.utils.translation import gettext as _
from drf_spectacular.utils import extend_schema
from rest_framework import exceptions, parsers, permissions, status, views
from rest_framework.response import Response

from api.passports.serializers import PassportBaseSerializer
from api.passports.services import passport_service
from common.documents import tasks
from common.documents.serializers import (
    DocumentOneImageSerializer,
    DocumentTwoImageRequestSerializer,
)


class AbstractPassportCreateView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.MultiPartParser,)

    def get_request_serializer(self, *args, **kwargs):
        raise NotImplementedError()

    def get_response_serializer(self, *args, **kwargs):
        return PassportBaseSerializer(*args, **kwargs)

    def validate_serializer(self, user, data):
        serializer = self.get_request_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        if passport_service.get(user_owner=user) is not None:
            raise exceptions.PermissionDenied([_("У вас уже есть документ")])

        return serializer


@extend_schema(
    request=DocumentTwoImageRequestSerializer,
    responses=PassportBaseSerializer(),
    tags=("documents",),
    summary="[renter] Загрузить паспорт нового образца",
    description="На вход принимает либо две фотографии (.jpg .png) в два поля. "
    "Либо один файл .pdf с двумя страницами",
)
class NewPassportCreateView(AbstractPassportCreateView):

    def get_request_serializer(self, *args, **kwargs):
        return DocumentTwoImageRequestSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        in_serializer = self.validate_serializer(request.user, request.data)
        validated_data = in_serializer.validated_data

        obj = passport_service.create_no_scan(
            user_owner=request.user,
            is_id_card=True,
            image_file=validated_data["image_file"],
            image_file_back=validated_data["image_file_back"],
        )

        if (image_file_back := validated_data["image_file_back"]) is None:
            image_file_back_name = None
        else:
            image_file_back_name = image_file_back.name

        tasks.scan_passport_new.delay(
            uuid=obj.pk,
            image_path_1=validated_data["image_file"].name,
            image_path_2=image_file_back_name,
        )

        out_serializer = self.get_response_serializer(obj)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    request=DocumentOneImageSerializer,
    responses=PassportBaseSerializer(),
    tags=("documents",),
    summary="[renter] Загрузить паспорт старого образца",
    description="На вход принимает один файл в формате .png .pdf .jpg",
)
class OldPassportCreateView(AbstractPassportCreateView):

    def get_request_serializer(self, *args, **kwargs):
        return DocumentOneImageSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        in_serializer = self.validate_serializer(request.user, request.data)
        validated_data = in_serializer.validated_data

        obj = passport_service.create_no_scan(
            user_owner=request.user,
            is_id_card=False,
            image_file=validated_data["image_file"],
            image_file_back=None,
        )

        tasks.scan_passport_old.delay(
            obj.pk,
            validated_data["image_file"].name,
        )

        out_serializer = self.get_response_serializer(obj)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)
