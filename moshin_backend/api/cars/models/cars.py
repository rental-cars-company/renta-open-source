from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _

from api.cars.models import CarFleet
from api.cars.validators import validate_year_value
from api.users.models import User
from common.constants import (
    CAR_CLASS_CHOICES,
    CAR_COLOR_CHOICES,
    CAR_TYPE_CHOICES,
    ENGINE_TYPE_CHOICES,
)
from common.models import ModelBase


class Cars(ModelBase):
    class Meta(ModelBase.Meta):
        verbose_name = _("машину")
        verbose_name_plural = _("Машины")
        ordering = ["-created_at"]

    fleet = models.ForeignKey(
        CarFleet,
        on_delete=models.CASCADE,
        related_name="cars",
        verbose_name=_("Автопарк"),
        null=True,
    )
    car_class = models.CharField(
        max_length=20,
        choices=CAR_CLASS_CHOICES,
        verbose_name=_("Класс авто (стандарт/премиум)"),
        default="standard",
    )
    brand = models.CharField(max_length=100, verbose_name=_("Марка"))
    model = models.CharField(max_length=100, verbose_name=_("Модель"))
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_("Цена за час"),
    )
    is_automatic = models.BooleanField(verbose_name=_("Автоматическая коробка"))
    engine_type = models.CharField(
        max_length=20,
        choices=ENGINE_TYPE_CHOICES,
        default="gasoline",
        verbose_name=_("Тип двигателя"),
    )
    year = models.PositiveSmallIntegerField(
        validators=[validate_year_value],
        verbose_name=_("Год выпуска"),
    )
    license_plate = models.CharField(
        max_length=20, verbose_name=_("Регистрационный номер")
    )
    color = models.CharField(
        max_length=20, choices=CAR_COLOR_CHOICES, verbose_name=_("Цвет")
    )
    required_age = models.PositiveSmallIntegerField(
        verbose_name=_("Минимальный возраст водителя"), default=18
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Добавлено")
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Изменено"))

    android_auto = models.BooleanField(
        default=False, verbose_name=_("Android Auto")
    )
    apple_car_play = models.BooleanField(
        default=False, verbose_name=_("Apple CarPlay")
    )
    child_seat = models.BooleanField(
        default=False, verbose_name=_("Детское кресло")
    )
    bluetooth = models.BooleanField(default=False, verbose_name=_("Bluetooth"))
    aux = models.BooleanField(default=False, verbose_name=_("AUX"))

    description = models.TextField(
        blank=True, null=True, verbose_name=_("Описание")
    )
    car_type = models.CharField(
        max_length=32,
        choices=CAR_TYPE_CHOICES,
        verbose_name=_("Тип кузова (sedan, suv и т.д.)"),
    )
    supports_pickup = models.BooleanField(
        default=True, verbose_name=_("Поддерживает самовывоз")
    )
    seats = models.SmallIntegerField(
        verbose_name=_("Количество посадочных мест")
    )
    has_conditioner = models.BooleanField(verbose_name=_("Имеет кондиционер"))

    def __str__(self):
        return f"{self.model} ({self.license_plate})"


class CarImage(ModelBase):
    car = models.ForeignKey(
        Cars, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="car_images/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]


class FavoriteCars(ModelBase):
    class Meta(ModelBase.Meta):
        abstract = False
        constraints = [
            UniqueConstraint(
                fields=["user", "car"], name="unique_fav_user_cars"
            )
        ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorites"
    )
    car = models.ForeignKey(
        Cars, on_delete=models.CASCADE, related_name="favorites"
    )

    def __str__(self):
        return _('Автомобиль "%(car)s" в избранном у %(user)s') % {
            "car": self.car,
            "user": self.user,
        }
