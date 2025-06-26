from django.db import models

from common.models import ModelBase


class AppVersion(ModelBase):
    PLATFORM_CHOICES = [
        ("android", "Android"),
        ("ios", "iOS"),
    ]

    platform = models.CharField(
        max_length=10, choices=PLATFORM_CHOICES, unique=True
    )
    version = models.CharField(max_length=20)
    link = models.URLField()

    def __str__(self):
        return f"{self.platform} — {self.version}"
