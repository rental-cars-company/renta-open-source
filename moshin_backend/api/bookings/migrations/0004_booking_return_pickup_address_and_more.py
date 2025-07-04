# Generated by Django 5.2 on 2025-05-13 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0003_booking_deposit"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="return_pickup_address",
            field=models.CharField(
                blank=True,
                max_length=255,
                null=True,
                verbose_name="Адрес возврата машины клиентом",
            ),
        ),
        migrations.AddField(
            model_name="booking",
            name="return_pickup_requested",
            field=models.BooleanField(
                default=False,
                help_text="Если True — клиент хочет, чтобы мы сами забрали машину по адресу",
                verbose_name="Забрать машину у клиента",
            ),
        ),
    ]
