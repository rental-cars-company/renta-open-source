# Register your models here.
from django.contrib import admin

from api.notifications.models import Device, Notification


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "push_token",
        "created_time",
    ]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "booking",
        "type",
        "message",
        "payload",
        "created_at",
        "is_read",
    ]
