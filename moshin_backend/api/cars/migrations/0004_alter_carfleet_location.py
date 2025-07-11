# Generated by Django 5.2 on 2025-05-05 16:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cars", "0003_alter_cars_car_type"),
        ("locations", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="carfleet",
            name="location",
            field=models.ForeignKey(
                default="ce16808d-4a3d-4a49-b3f7-5fc6612523bc",
                on_delete=django.db.models.deletion.CASCADE,
                to="locations.location",
                verbose_name="Пункт выдачи (location)",
            ),
            preserve_default=False,
        ),
    ]
