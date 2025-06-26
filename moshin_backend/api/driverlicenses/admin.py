from django.contrib import admin

from api.driverlicenses.models import DriverLicense


@admin.register(DriverLicense)
class PassportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "validation_status",
        "name",
        "surname",
        "serial_number",
    )
