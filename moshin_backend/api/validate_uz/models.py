from django.db import models
from django.utils.translation import gettext_lazy as _

from api.users.models import User


class ValidateUz(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь"),
        related_name="validateuz",
    )
    passport = models.CharField(
        blank=True,
        null=True,
        max_length=9,
        verbose_name=_("Паспорт (серия и номер)"),
    )
    fio = models.CharField(
        blank=True, null=True, max_length=64, verbose_name=_("ФИО (полностью)")
    )
    surname = models.CharField(
        blank=True, null=True, max_length=24, verbose_name=_("Фамилия")
    )
    name = models.CharField(
        blank=True, null=True, max_length=24, verbose_name=_("Имя")
    )
    middlename = models.CharField(
        blank=True, null=True, max_length=24, verbose_name=_("Отчество")
    )
    date_of_birth = models.DateField(
        blank=True, null=True, verbose_name=_("Дата рождения")
    )

    dl_begin = models.DateField(
        blank=True, null=True, verbose_name=_("Дата выдачи ВУ")
    )
    dl_end = models.DateField(
        blank=True, null=True, verbose_name=_("Срок действия ВУ до")
    )
    dl_issued_by = models.CharField(
        blank=True, null=True, max_length=128, verbose_name=_("Кем выдано ВУ")
    )
    dl_serial_number = models.CharField(
        blank=True, null=True, max_length=9, verbose_name=_("Серия и номер ВУ")
    )
    dl_category = models.CharField(
        blank=True, null=True, max_length=16, verbose_name=_("Категория ВУ")
    )
    dl_category_begin = models.DateField(
        blank=True, null=True, verbose_name=_("Начало действия категории")
    )
    dl_category_end = models.DateField(
        blank=True, null=True, verbose_name=_("Окончание действия категории")
    )

    birth_region_id = models.IntegerField(
        blank=True, null=True, verbose_name=_("ID региона рождения")
    )
    birth_city_id = models.IntegerField(
        blank=True, null=True, verbose_name=_("ID города рождения")
    )
    birth_place = models.CharField(
        blank=True, null=True, max_length=64, verbose_name=_("Место рождения")
    )
    address_region_id = models.IntegerField(
        blank=True, null=True, verbose_name=_("ID региона адреса проживания")
    )
    address_city_id = models.IntegerField(
        blank=True, null=True, verbose_name=_("ID города адреса проживания")
    )
    address_place = models.CharField(
        blank=True,
        null=True,
        max_length=128,
        verbose_name=_("Адрес проживания (улица, дом)"),
    )

    debts_sum = models.IntegerField(
        blank=True, null=True, verbose_name=_("Сумма долгов")
    )

    class Meta:
        verbose_name = _("данные из validate.uz")
        verbose_name_plural = _("Данные из validate.uz")
