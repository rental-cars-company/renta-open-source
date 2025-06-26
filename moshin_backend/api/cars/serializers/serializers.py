import uuid

from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from api.cars.models import CarFleet, CarImage, Cars
from api.cars.serializers import CarFleetSerializer
from api.cars.validators import (
    validate_license_plate_format,
    validate_year_value,
)
from common.validators import validate_positive


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ["id", "image", "order"]


class CarsSerializer(serializers.ModelSerializer):
    fleet = serializers.PrimaryKeyRelatedField(queryset=CarFleet.objects.all())
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, validators=[validate_positive]
    )
    is_automatic = serializers.BooleanField(allow_null=True)
    images = CarImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    deleted_images = serializers.CharField(write_only=True, required=False)
    color_display = serializers.CharField(
        source="get_color_display", read_only=True
    )
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Cars
        fields = [
            "id",
            "fleet",
            "car_class",
            "brand",
            "model",
            "price",
            "is_automatic",
            "year",
            "license_plate",
            "color",
            "color_display",
            "created_at",
            "updated_at",
            # images = read-only, uploaded_images = write-only
            "images",
            "uploaded_images",
            "deleted_images",
            "android_auto",
            "apple_car_play",
            "child_seat",
            "bluetooth",
            "aux",
            "description",
            "car_type",
            "engine_type",
            "seats",
            "has_conditioner",
            "is_favorite",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def _process_uploaded_images(self, car, uploaded_images):
        from rest_framework.exceptions import ValidationError

        if not uploaded_images:
            return

        existing_orders = list(
            CarImage.objects.filter(car=car).values_list("order", flat=True)
        )

        available_orders = [i for i in range(10) if i not in existing_orders]

        if len(available_orders) < len(uploaded_images):
            raise ValidationError(
                _(
                    "Можно загрузить максимум 10 изображений. Удалите старые, чтобы загрузить новые."
                )
            )

        for image in uploaded_images:
            try:
                next_order = available_orders.pop(0)
                try:
                    CarImage.objects.create(
                        car=car, image=image, order=next_order
                    )
                except IntegrityError:
                    raise ValidationError(
                        _("Изображение с таким порядком уже существует.")
                    )
                except Exception:
                    raise ValidationError(
                        _("Файл не является допустимым изображением.")
                    )
            except Exception:
                raise ValidationError(
                    _("Файл не является допустимым изображением.")
                )

    def to_representation(self, instance):
        """Вернуть полную информацию о fleet вместо id."""
        representation = super().to_representation(instance)
        fleet_instance = instance.fleet
        representation["fleet"] = CarFleetSerializer(
            fleet_instance, context=self.context
        ).data
        return representation

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", [])
        car = Cars.objects.create(**validated_data)
        self._process_uploaded_images(car, uploaded_images)
        return car

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", None)
        deleted_images = validated_data.pop("deleted_images", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if uploaded_images is not None:
            self._process_uploaded_images(instance, uploaded_images)

        if deleted_images:
            CarImage.objects.filter(
                id__in=deleted_images, car=instance
            ).delete()

        return instance

    def validate_year(self, value):
        try:
            return validate_year_value(value)
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def validate_license_plate(self, value):
        try:
            return validate_license_plate_format(value)
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def validate_is_automatic(self, value):
        if value is None:
            raise serializers.ValidationError(
                _("Это поле обязательно и должно быть True или False.")
            )
        return value

    def validate_deleted_images(self, value):
        try:
            return [uuid.UUID(x.strip()) for x in value.split(",") if x.strip()]
        except ValueError:
            raise serializers.ValidationError(
                _("Список содержит невалидные UUID.")
            )

    def get_is_favorite(self, obj) -> bool:
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            return False
        return obj.favorites.filter(user=request.user).exists()


class FavoriteCarsSerializer(serializers.ModelSerializer):
    """Сериализатор для краткой информации об автомобилях в избранном."""

    images = CarImageSerializer(many=True, read_only=True)

    class Meta:
        model = Cars
        fields = ["id", "brand", "model", "price", "year", "images"]


class YearsSerializer(serializers.Serializer):
    years = serializers.ListField(
        child=serializers.IntegerField(),
        # read_only=True,
    )


class BrandsSerializer(serializers.Serializer):
    brands = serializers.ListField(
        child=serializers.CharField(),
        # read_only=True,
    )
