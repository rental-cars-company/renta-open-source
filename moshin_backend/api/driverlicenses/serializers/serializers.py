from rest_framework import serializers

from api.driverlicenses.models import DriverLicense
from api.validate_uz.models import ValidateUz
from api.validate_uz.serializers import ValidateUzSerializer


class DriverLicenseBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverLicense
        fields = (
            "id",
            "user",
            "surname",
            "name",
            "date_of_birth",
            "serial_number",
            "acquire_date",
            "validity_period",
            "has_b_category",
            "image_file",
            "image_file_back",
            "created_time",
            "updated_time",
            "validation_status",
        )
        read_only_fields = ("id", "user", "image_file", "image_file_back")


class DriverLicenseAdminSerializer(DriverLicenseBaseSerializer):
    validate_uz = serializers.SerializerMethodField()

    class Meta(DriverLicenseBaseSerializer.Meta):
        fields = DriverLicenseBaseSerializer.Meta.fields + ("validate_uz",)
        read_only_fields = DriverLicenseBaseSerializer.Meta.read_only_fields + (
            "validate_uz",
        )

    def get_validate_uz(self, obj):
        try:
            validate_uz = ValidateUz.objects.get(user=obj.user)
            return ValidateUzSerializer(validate_uz).data
        except ValidateUz.DoesNotExist:
            return None
