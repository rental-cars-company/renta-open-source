from django.contrib import admin

from api.locations.models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["id", "address", "latitude", "longitude"]
