from typing import TYPE_CHECKING

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from api.users.models.manager import UserManager
from api.users.models.roles import USER_ROLE_CHOICES, USER_ROLE_RENTER
from api.users.validators import profile_photo_extension_validator
from common.constants import USER_PROFILE_MEDIA_DIR
from common.models import ModelBase
from common.validators import minimum_age_validator, uz_phone_format_validator

if TYPE_CHECKING:
    from api.driverlicenses.models import DriverLicense
    from api.passports.models import Passport
    from api.referral.models import ReferralInfo


class User(ModelBase, AbstractUser):
    referral: "ReferralInfo"
    passport: "Passport"
    driverlicenses: "DriverLicense"

    class Meta(ModelBase.Meta):
        abstract = False
        verbose_name = _("пользователя")
        verbose_name_plural = _("Пользователи")

    LANGUAGE_CHOICES = (
        ("ru", "Русский"),
        ("uz", "Oʻzbekcha"),
        ("en", "English"),
    )
    language = models.CharField(
        _("Язык интерфейса"),
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default="uz",
    )

    role = models.CharField(
        verbose_name=_("Роль"),
        choices=USER_ROLE_CHOICES,
        default=USER_ROLE_RENTER,
    )

    phone = models.CharField(
        verbose_name=_("Номер телефона"),
        validators=(uz_phone_format_validator,),
        null=True,
        unique=True,
        blank=True,
    )
    username = models.CharField(
        verbose_name=_("Имя пользователя"),
        max_length=150,
        unique=True,
        null=True,
        blank=True,
    )

    REQUIRED_FIELDS = [
        "password",
    ]

    fcm_token = models.TextField(
        _("FCM токен устройства"), null=True, blank=True
    )
    name = models.CharField(_("Имя по паспорту"), null=True, blank=True)
    surname = models.CharField(_("Фамилия по паспорту"), null=True, blank=True)

    age = models.IntegerField(
        _("Возраст"),
        validators=(minimum_age_validator,),
        blank=True,
        null=True,
    )

    profile_image = models.FileField(
        verbose_name=_("Фото профиля"),
        upload_to=USER_PROFILE_MEDIA_DIR,
        blank=True,
        null=True,
        validators=(profile_photo_extension_validator,),
    )

    objects: UserManager = UserManager()  # type: ignore

    def __str__(self):
        if self.role == USER_ROLE_RENTER:
            return f"{self.role} {self.phone}"
        return f"{self.role} {self.username}"
