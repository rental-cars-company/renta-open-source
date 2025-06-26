from rest_framework import serializers

from api.notifications.models import Device, Notification


class NotificationSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source="booking.car.brand", read_only=True)
    model = serializers.CharField(source="booking.car.model", read_only=True)
    delivery_option = serializers.CharField(
        source="booking.delivery_option", read_only=True
    )
    booking_id = serializers.IntegerField(source="booking.id", read_only=True)
    created_time = serializers.DateTimeField(
        source="created_at", read_only=True
    )
    status = serializers.CharField(source="booking_status", read_only=True)

    class Meta:
        model = Notification
        fields = (
            "brand",
            "model",
            "delivery_option",
            "booking_id",
            "created_time",
            "status",
        )


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ("id", "push_token", "push_enabled", "updated_at")
        read_only_fields = ("updated_at",)
