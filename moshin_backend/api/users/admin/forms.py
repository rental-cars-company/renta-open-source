from django import forms
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions as drf_exceptions

from ..models import (
    USER_ROLE_ADMIN,
    USER_ROLE_RENTER,
    USER_ROLE_SUPERUSER,
    User,
)


class UserAdminForm(forms.ModelForm):
    REQUIRED_FIELDS_FOR_ROLES = {
        USER_ROLE_RENTER: ("phone",),
        USER_ROLE_ADMIN: (
            "password",
            "username",
        ),
        USER_ROLE_SUPERUSER: (
            "password",
            "username",
        ),
    }

    class Meta:
        model = User
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].required = False

    def clean(self):
        cleaned_data: dict = super().clean()  # type: ignore

        # чтобы пустые значения стали None
        cleaned_data["password"] = cleaned_data.get("password")
        cleaned_data["username"] = cleaned_data.get("username")
        cleaned_data["phone"] = cleaned_data.get("phone")
        #

        role: str = cleaned_data["role"]
        required_fields = self.REQUIRED_FIELDS_FOR_ROLES[role]
        for required in required_fields:
            if required not in cleaned_data or not cleaned_data[required]:
                self.add_error(
                    required,
                    forms.ValidationError(
                        _(f"Роль {role} требует поле {required}")
                    ),
                )

        return cleaned_data

    def full_clean(self) -> None:
        try:
            return super().full_clean()
        except drf_exceptions.ValidationError as _e:
            self.add_error(
                None,
                forms.ValidationError(message=_e.detail, code=_e.default_code),
            )
