import os
from typing import Sequence

import fitz
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .validators import document_file_extension_validator

SIZE_LIMIT_MB = 10
SIZE_LIMIT_BYTES = SIZE_LIMIT_MB * 1024 * 1024  # 10мб
IMG_SAVE_MODE = "RGB"


class DocumentOneImageSerializer(serializers.Serializer):
    image_file = serializers.FileField(
        validators=(document_file_extension_validator,)
    )

    def validate_file_sizes(self, files: Sequence[InMemoryUploadedFile | None]):
        for file in files:
            if file and file.size and file.size > SIZE_LIMIT_BYTES:
                raise serializers.ValidationError(
                    detail=[
                        _(f"Превышен лимит размера файла ({SIZE_LIMIT_MB}мб)")
                    ]
                )

    def validate(self, attrs):
        validated_data: dict = super().validate(attrs)  # type: ignore

        image_file_1: InMemoryUploadedFile = validated_data["image_file"]
        self.validate_file_sizes((image_file_1,))
        extension_1 = os.path.splitext(str(image_file_1))[1]

        if extension_1 != ".pdf":
            return validated_data

        file = fitz.open(stream=image_file_1.read())
        if file.page_count > 2:
            raise serializers.ValidationError(
                [_("PDF файл содержит слишком много страниц")]
            )
        if file.page_count == 0:
            raise serializers.ValidationError([_("PDF файл пуст")])
        return validated_data


class DocumentTwoImageRequestSerializer(DocumentOneImageSerializer):
    image_file_back = serializers.FileField(
        validators=(document_file_extension_validator,),
        required=False,
        default=None,
    )
    default_error_messages = {
        "files": _(
            "Необходимо предоставить либо "
            "два фото (спереди и сзади в формате .png, .jpg) "
            "либо .pdf файл с двумя страницами"
        )
    }

    def validate(self, attrs):
        validated_data: dict = serializers.Serializer.validate(
            self, attrs
        )  # type: ignore

        image_file_1: InMemoryUploadedFile = validated_data["image_file"]
        image_file_2: InMemoryUploadedFile | None = validated_data.get(
            "image_file_back", None
        )
        self.validate_file_sizes((image_file_1, image_file_2))

        extension_1 = os.path.splitext(str(image_file_1))[1]

        if image_file_2 is None:

            if extension_1 != ".pdf":
                raise serializers.ValidationError(
                    [self.default_error_messages["files"]]
                )

            pdf_file = fitz.open(stream=image_file_1.read())
            if pdf_file.page_count != 2:
                raise serializers.ValidationError(
                    [self.default_error_messages["files"]]
                )

        return validated_data
