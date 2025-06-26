from django.db import models
from django.utils.translation import gettext_lazy as _

from api.users.models import User
from common.constants import DRIVERLICENSES_MEDIA_DIR
from common.documents.models import DocumentBase
from common.documents.validators import document_file_extension_validator


class DriverLicense(DocumentBase):
    class Meta(DocumentBase.Meta):
        abstract = False
        verbose_name = _("Водительские права")
        verbose_name_plural = _("Водительские права")

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь. Владелец прав"),
        related_name="driverlicense",
    )

    #
    surname = models.CharField(
        verbose_name=_("Фамилия (1)"), blank=True, null=True
    )
    name = models.CharField(verbose_name=_("Имя (2)"), blank=True, null=True)
    date_of_birth = models.DateField(
        verbose_name=_("Дата рождения (3)"), blank=True, null=True
    )
    acquire_date = models.DateField(
        verbose_name=_("Дата получения (4a)"), blank=True, null=True
    )
    validity_period = models.CharField(
        verbose_name=_("Срок действия (4b)"), blank=True, null=True
    )
    has_b_category = models.BooleanField(
        verbose_name=_("Имеет ли B категорию (9)"), blank=True, null=True
    )
    serial_number = models.CharField(
        verbose_name=_("Серийный номер (10)"),
        unique=True,
        blank=True,
        null=True,
    )
    #

    image_file = models.FileField(
        verbose_name=_("Фото прав"),
        upload_to=DRIVERLICENSES_MEDIA_DIR,
        null=False,
        blank=True,
        validators=(document_file_extension_validator,),
    )
    image_file_back = models.FileField(
        verbose_name=_("Фото прав сзади"),
        upload_to=DRIVERLICENSES_MEDIA_DIR,
        null=True,
        blank=True,
        validators=(document_file_extension_validator,),
    )

    def __str__(self) -> str:
        return f"{_("Права")} {self.user}"
