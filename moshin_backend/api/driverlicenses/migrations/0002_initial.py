# Generated by Django 5.2 on 2025-04-30 15:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("driverlicenses", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="driverlicense",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="driverlicense",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь. Владелец прав",
            ),
        ),
    ]
