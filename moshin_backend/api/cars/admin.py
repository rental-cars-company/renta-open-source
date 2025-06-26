from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from api.cars.forms import CarsAdminForm
from api.cars.models import CarFleet, CarImage, Cars


@admin.register(CarFleet)
class CarFleetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "owner_phone_number",
        "get_pickup_address",
    )
    search_fields = ("id", "name", "owner_phone_number", "location__address")
    list_filter = ("owner_phone_number",)

    def get_pickup_address(self, obj):
        return obj.location.address if obj.location else "-"

    get_pickup_address.short_description = _("Pickup Address")


class LimitedImageInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        total_forms = 0
        for form in self.forms:
            if not form.cleaned_data.get("DELETE", False) and form.cleaned_data:
                total_forms += 1

        if total_forms > 10:
            raise ValidationError(
                _("Нельзя добавить больше 10 изображений к одному автомобилю.")
            )


class CarImageInline(admin.TabularInline):
    model = CarImage
    formset = LimitedImageInlineFormSet
    extra = 0
    readonly_fields = ["preview"]

    def preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="max-height: 100px;" />'
            )
        return "-"

    preview.short_description = _("Превью")


class CarsAdmin(admin.ModelAdmin):
    form = CarsAdminForm
    inlines = [CarImageInline]

    list_display = [
        "brand",
        "id",
        "model",
        "is_automatic",
        "year",
        "license_plate",
        "color",
        "car_type",
        "android_auto",
        "apple_car_play",
        "bluetooth",
        "created_at",
        "updated_at",
        "supports_pickup",
    ]

    search_fields = [
        "model",
        "license_plate",
        "color",
        "description",
        "car_type",
    ]

    list_filter = [
        "is_automatic",
        "color",
        "car_type",
        "android_auto",
        "apple_car_play",
        "child_seat",
        "bluetooth",
        "aux",
    ]

    readonly_fields = ["created_at", "updated_at"]


admin.site.register(Cars, CarsAdmin)
