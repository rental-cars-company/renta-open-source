# Generated by Django 5.2 on 2025-05-26 17:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cars", "0006_remove_cars_supports_delivery"),
    ]

    operations = [
        migrations.AlterField(
            model_name="carfleet",
            name="owner_phone_number",
            field=models.CharField(
                max_length=20,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Неверный номер",
                        regex="^\\+998(9[0-1]|9[3-5]|9[7-9]|33|55|77|88)[0-9]{7}$",
                    )
                ],
                verbose_name="Номер телефона (+998)",
            ),
        ),
    ]
