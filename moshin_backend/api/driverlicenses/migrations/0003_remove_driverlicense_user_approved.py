# Generated by Django 5.2 on 2025-05-04 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("driverlicenses", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="driverlicense",
            name="user_approved",
        ),
    ]
