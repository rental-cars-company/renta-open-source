from django.db import models
from django.utils.translation import gettext_lazy as _

from api.passports.validators import get_passport_pinfl_validators
from api.users.models import User
from common.constants import PASSPORTS_MEDIA_DIR
from common.documents.models import DocumentBase
from common.documents.validators import document_file_extension_validator


class Passport(DocumentBase):
    class Meta(DocumentBase.Meta):
        abstract = False
        verbose_name = _("Паспорт")
        verbose_name_plural = _("Паспорта")

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь. Владелец паспорта"),
        related_name="passport",
    )

    #
    is_id_card = models.BooleanField(
        verbose_name=_("Является ли ID картой"), default=True
    )
    name = models.CharField(verbose_name=_("Имя"), blank=True, null=True)
    surname = models.CharField(verbose_name=_("Фамилия"), blank=True, null=True)
    middlename = models.CharField(
        verbose_name=_("Отчество"), blank=True, null=True
    )
    pinfl = models.BigIntegerField(
        verbose_name=_("ПИНФЛ"),
        blank=True,
        null=True,
        unique=True,
        validators=get_passport_pinfl_validators(),
    )
    date_of_birth = models.DateField(
        verbose_name=_("Дата рождения"), blank=True, null=True
    )
    serial_and_number = models.CharField(
        verbose_name=_("Серия и номер паспорта"), blank=True, null=True
    )

    image_file = models.FileField(
        verbose_name=_("Фото паспорта"),
        upload_to=PASSPORTS_MEDIA_DIR,
        blank=True,
        null=False,
        validators=(document_file_extension_validator,),
    )
    image_file_back = models.FileField(
        verbose_name=_("Фото паспорта сзади (если ID карта)"),
        upload_to=PASSPORTS_MEDIA_DIR,
        null=True,
        blank=True,
        validators=(document_file_extension_validator,),
    )

    def __str__(self) -> str:
        return f"{_("Паспорт")} {self.user}"
