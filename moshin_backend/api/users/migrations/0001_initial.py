# Generated by Django 5.2 on 2025-04-30 15:58

import common.validators
import django.core.validators
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "password",
                    models.CharField(max_length=128, verbose_name="password"),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="date joined",
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="uuid",
                    ),
                ),
                ("created_time", models.DateTimeField(auto_now_add=True)),
                ("updated_time", models.DateTimeField(auto_now=True)),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("renter", "Пользователь"),
                            ("admin", "Администратор"),
                            ("superuser", "Суперпользователь"),
                        ],
                        default="renter",
                        verbose_name="Роль",
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True,
                        null=True,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Номер телефона неверного формата. Он должен начинаться с +998",
                                regex="^\\+998(9[0-1]|9[3-5]|9[7-9]|33|55|77|88)[0-9]{7}$",
                            )
                        ],
                        verbose_name="Номер телефона",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        blank=True,
                        max_length=150,
                        null=True,
                        unique=True,
                        verbose_name="Имя пользователя",
                    ),
                ),
                (
                    "fcm_token",
                    models.TextField(
                        blank=True,
                        null=True,
                        verbose_name="FCM токен устройства",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True, null=True, verbose_name="Имя по паспорту"
                    ),
                ),
                (
                    "surname",
                    models.CharField(
                        blank=True,
                        null=True,
                        verbose_name="Фамилия по паспорту",
                    ),
                ),
                (
                    "date_of_birth",
                    models.DateField(
                        blank=True,
                        null=True,
                        validators=[common.validators.minimum_age_validator],
                        verbose_name="Дата рождения",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "пользователя",
                "verbose_name_plural": "Пользователи",
                "ordering": ["-updated_time"],
                "abstract": False,
            },
        ),
    ]
