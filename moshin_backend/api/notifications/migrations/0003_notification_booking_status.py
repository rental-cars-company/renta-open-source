# Generated by Django 5.2.1 on 2025-06-14 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notifications", "0002_alter_device_unique_together"),
    ]

    operations = [
        migrations.AddField(
            model_name="notification",
            name="booking_status",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
