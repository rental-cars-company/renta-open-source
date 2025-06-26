from typing import Optional

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from api.bookings.models import Booking
from api.cars.serializers import CarsSerializer
from api.payments.models import Payment  # подключаем модель Payment
from api.users.serializers import UserSerializer
from api.validate_uz.models import ValidateUz
from api.validate_uz.serializers import ValidateUzSerializer

from .details import BookingDetailsSerializer


class BookingBaseSerializer(serializers.ModelSerializer):
    rental_summary = serializers.SerializerMethodField(
        help_text=_("Детализированная сводка по стоимости аренды"),
    )
    payment_method = serializers.CharField(read_only=True)

    @extend_schema_field(BookingDetailsSerializer)
    def get_rental_summary(self, obj: Booking):
        return obj.rental_summary

    class Meta:
        model = Booking
        fields = (
            "id",
            "car",
            "user",
            "coupon",
            "status",
            "rental_summary",
            "payment_method",
            "start_datetime",
            "end_datetime",
            "delivery_option",
            "delivery_latitude",
            "delivery_longitude",
            "return_pickup_requested",
            "return_pickup_address",
            "driver_requested",
            "created_time",
            "updated_time",
        )
        read_only_fields = (
            "user",
            "status",
            "rental_summary",
            "payment_method",
            "created_time",
            "updated_time",
        )


class BookingCreateSerializer(BookingBaseSerializer):
    def validate(self, attrs):
        start = attrs.get("start_datetime")
        end = attrs.get("end_datetime")
        car = attrs.get("car")
        option = attrs.get("delivery_option")

        if start >= end:
            raise serializers.ValidationError(
                _("Дата начала должна быть раньше даты окончания.")
            )

        if start <= timezone.now():
            raise serializers.ValidationError(
                _("Нельзя бронировать в прошлом.")
            )

        if option == "pickup":
            if not car.supports_pickup:
                raise serializers.ValidationError(
                    _("Это авто нельзя забрать самостоятельно.")
                )
            attrs["delivery_latitude"] = None
            attrs["delivery_longitude"] = None

        elif option == "delivery":
            lat = attrs.get("delivery_latitude")
            long = attrs.get("delivery_longitude")
            if lat is None or long is None:
                raise serializers.ValidationError(
                    _("Координаты доставки обязательны.")
                )

            attrs["delivery_price"] = 50000

        if attrs.get("return_pickup_requested") and not attrs.get(
            "return_pickup_address"
        ):
            raise serializers.ValidationError(
                _("Укажите адрес, если хотите, чтобы мы забрали машину.")
            )

        return attrs


class BookingReadSerializer(BookingBaseSerializer):
    car = CarsSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    # DELIVERY LATITUDE
    delivery_latitude = serializers.FloatField(
        read_only=True, allow_null=True, default=0.0
    )
    # DELIVERY LONGITUDE
    delivery_longitude = serializers.FloatField(
        read_only=True, allow_null=True, default=0.0
    )

    # Новые поля: полный PAN и «сырое» expiry
    card_pan = serializers.SerializerMethodField(read_only=True)
    card_expiry = serializers.SerializerMethodField(read_only=True)

    class Meta(BookingBaseSerializer.Meta):
        fields = BookingBaseSerializer.Meta.fields + (
            "delivery_latitude",
            "delivery_longitude",
            "card_pan",
            "card_expiry",
        )
        read_only_fields = fields

    def get_delivery_latitude(self, obj):
        return (
            obj.delivery_latitude if obj.delivery_latitude is not None else 0.0
        )

    def get_delivery_longitude(self, obj):
        return (
            obj.delivery_longitude
            if obj.delivery_longitude is not None
            else 0.0
        )

    def _get_latest_success_card_payment(
        self, booking: Booking
    ) -> Optional[Payment]:
        """Возвращает последний успешный карточный платеж для бронирования."""
        return (
            Payment.objects.filter(
                booking=booking,
                status=Payment.Status.SUCCESS,
                method=Payment.Method.CARD,
            )
            .order_by("-created_time")
            .first()
        )

    def get_card_pan(self, obj: Booking) -> Optional[str]:
        payment = self._get_latest_success_card_payment(obj)
        return getattr(payment, "pan", None) if payment else None

    def get_card_expiry(self, obj: Booking) -> Optional[str]:
        payment = self._get_latest_success_card_payment(obj)
        return getattr(payment, "expiry", None) if payment else None


class BookingAdminReadSerializer(BookingReadSerializer):
    """Если user=admin — добавляются данные из validate.uz и hold_success_id."""

    validate_uz = serializers.SerializerMethodField()
    hold_success_id = serializers.SerializerMethodField()

    class Meta(BookingReadSerializer.Meta):
        fields = BookingReadSerializer.Meta.fields + (
            "validate_uz",
            "hold_success_id",
        )
        read_only_fields = fields

    @extend_schema_field(ValidateUzSerializer)
    def get_validate_uz(self, obj):
        try:
            validate_uz = ValidateUz.objects.get(user=obj.user)
            return ValidateUzSerializer(validate_uz).data
        except ValidateUz.DoesNotExist:
            return None

    @extend_schema_field(serializers.IntegerField())
    def get_hold_success_id(self, obj: Booking):
        payment_with_hold = (
            obj.payments.filter(hold_success_id__isnull=False)
            .order_by("-created_time")
            .first()
        )
        if payment_with_hold:
            return payment_with_hold.hold_success_id
        return None


class BookingStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["status"]
