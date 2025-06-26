from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import ModelBase


class Location(ModelBase):

    class Meta(ModelBase.Meta):
        abstract = False
        verbose_name = _("Локация")
        verbose_name_plural = _("Локации")
        app_label = "locations"

    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.address or f"{self.latitude}, {self.longitude}"
