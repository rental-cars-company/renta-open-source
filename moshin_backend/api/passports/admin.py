from django.contrib import admin

from api.passports.models.models import Passport


@admin.register(Passport)
class PassportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "validation_status",
        "pinfl",
        "is_id_card",
        "name",
        "surname",
        "middlename",
        "serial_and_number",
    )
