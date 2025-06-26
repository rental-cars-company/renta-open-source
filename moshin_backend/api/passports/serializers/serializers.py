from rest_framework import serializers

from api.passports.models import Passport
from api.validate_uz.models import ValidateUz
from api.validate_uz.serializers import ValidateUzSerializer


class PassportBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passport
        fields = (
            "id",
            "user",
            "is_id_card",
            "validation_status",
            "name",
            "surname",
            "middlename",
            "pinfl",
            "date_of_birth",
            "serial_and_number",
            "image_file",
            "image_file_back",
            "created_time",
            "updated_time",
        )
        read_only_fields = ("id", "user", "image_file", "image_file_back")


class PassportAdminSerializer(PassportBaseSerializer):
    validate_uz = serializers.SerializerMethodField()

    class Meta(PassportBaseSerializer.Meta):
        fields = PassportBaseSerializer.Meta.fields + ("validate_uz",)
        read_only_fields = PassportBaseSerializer.Meta.read_only_fields + (
            "validate_uz",
        )

    def get_validate_uz(self, obj):
        try:
            validate_uz = ValidateUz.objects.get(user=obj.user)
            return ValidateUzSerializer(validate_uz).data
        except ValidateUz.DoesNotExist:
            return None
