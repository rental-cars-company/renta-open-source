# Generated by Django 5.2 on 2025-05-04 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("driverlicenses", "0003_remove_driverlicense_user_approved"),
    ]

    operations = [
        migrations.AlterField(
            model_name="driverlicense",
            name="serial_number",
            field=models.CharField(
                blank=True,
                null=True,
                unique=True,
                verbose_name="Серийный номер (10)",
            ),
        ),
    ]
