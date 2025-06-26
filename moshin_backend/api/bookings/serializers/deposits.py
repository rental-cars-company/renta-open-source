from rest_framework import serializers

from api.bookings.models import Deposit


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ["id", "user", "deposit", "created_time"]
        read_only_fields = ["id", "created_time"]
