# Generated by Django 5.2 on 2025-05-08 07:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ValidateUz",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "passport",
                    models.CharField(
                        blank=True,
                        max_length=9,
                        null=True,
                        verbose_name="Паспорт (серия и номер)",
                    ),
                ),
                (
                    "fio",
                    models.CharField(
                        blank=True,
                        max_length=64,
                        null=True,
                        verbose_name="ФИО (полностью)",
                    ),
                ),
                (
                    "surname",
                    models.CharField(
                        blank=True,
                        max_length=24,
                        null=True,
                        verbose_name="Фамилия",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True, max_length=24, null=True, verbose_name="Имя"
                    ),
                ),
                (
                    "middlename",
                    models.CharField(
                        blank=True,
                        max_length=24,
                        null=True,
                        verbose_name="Отчество",
                    ),
                ),
                (
                    "date_of_birth",
                    models.DateField(
                        blank=True, null=True, verbose_name="Дата рождения"
                    ),
                ),
                (
                    "dl_begin",
                    models.DateField(
                        blank=True, null=True, verbose_name="Дата выдачи ВУ"
                    ),
                ),
                (
                    "dl_end",
                    models.DateField(
                        blank=True,
                        null=True,
                        verbose_name="Срок действия ВУ до",
                    ),
                ),
                (
                    "dl_issued_by",
                    models.CharField(
                        blank=True,
                        max_length=128,
                        null=True,
                        verbose_name="Кем выдано ВУ",
                    ),
                ),
                (
                    "dl_serial_number",
                    models.CharField(
                        blank=True,
                        max_length=9,
                        null=True,
                        verbose_name="Серия и номер ВУ",
                    ),
                ),
                (
                    "dl_category",
                    models.CharField(
                        blank=True,
                        max_length=16,
                        null=True,
                        verbose_name="Категория ВУ",
                    ),
                ),
                (
                    "dl_category_begin",
                    models.DateField(
                        blank=True,
                        null=True,
                        verbose_name="Начало действия категории",
                    ),
                ),
                (
                    "dl_category_end",
                    models.DateField(
                        blank=True,
                        null=True,
                        verbose_name="Окончание действия категории",
                    ),
                ),
                (
                    "birth_region_id",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        verbose_name="ID региона рождения",
                    ),
                ),
                (
                    "birth_city_id",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="ID города рождения"
                    ),
                ),
                (
                    "birth_place",
                    models.CharField(
                        blank=True,
                        max_length=64,
                        null=True,
                        verbose_name="Место рождения",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "данные из validate_uz",
                "verbose_name_plural": "Данные из validate_uz",
            },
        ),
    ]
