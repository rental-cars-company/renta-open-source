from rest_framework import serializers

from api.validate_uz.models import ValidateUz


class ValidateUzSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValidateUz
        fields = "__all__"
