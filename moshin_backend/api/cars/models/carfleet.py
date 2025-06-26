from django.db import models
from django.utils.translation import gettext_lazy as _

from api.locations.models import Location
from common.models import ModelBase
from common.validators import uz_phone_format_validator


class CarFleet(ModelBase):
    class Meta(ModelBase.Meta):
        abstract = False
        verbose_name = _("автопарк")
        verbose_name_plural = _("Автопарки")

    name = models.CharField(max_length=128, verbose_name=_("Название компании"))
    owner_phone_number = models.CharField(
        max_length=20,
        verbose_name=_("Номер телефона (+998)"),
        validators=(uz_phone_format_validator,),
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        verbose_name=_("Пункт выдачи (location)"),
    )

    def __str__(self):
        return _("Автопарк: %(name)s") % {"name": self.name}
