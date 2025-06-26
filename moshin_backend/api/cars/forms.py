from datetime import datetime

from django import forms
from django.utils.translation import gettext_lazy as _

from api.cars.models import Cars
from api.cars.validators import (
    normalize_phone_number,
    validate_license_plate_format,
    validate_year_value,
)


class CarsAdminForm(forms.ModelForm):
    class Meta:
        model = Cars
        fields = "__all__"

    year = forms.TypedChoiceField(
        coerce=int,
        choices=[(y, y) for y in range(1980, datetime.now().year + 1)],
        required=True,
        label=_("Год выпуска"),
    )

    def clean_year(self):
        year = self.cleaned_data["year"]
        try:
            return validate_year_value(year)
        except ValueError as e:
            raise forms.ValidationError(str(e))

    def clean_license_plate(self):
        plate = self.cleaned_data["license_plate"]
        try:
            return validate_license_plate_format(plate)
        except ValueError as e:
            raise forms.ValidationError(str(e))

    def clean_owner_phone_number(self):
        phone = self.cleaned_data["owner_phone_number"]
        try:
            return normalize_phone_number(phone)
        except ValueError as e:
            raise forms.ValidationError(str(e))

    def clean(self):
        cleaned_data = super().clean()
        from_time = cleaned_data.get("available_from")
        to_time = cleaned_data.get("available_to")

        if from_time and to_time and from_time >= to_time:
            raise forms.ValidationError(
                _("Время 'доступно с' должно быть раньше 'доступно до'.")
            )
        return cleaned_data
