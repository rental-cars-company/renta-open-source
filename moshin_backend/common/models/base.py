from uuid import uuid4

from django.db import models


class ModelBase(models.Model):
    id = models.UUIDField(
        primary_key=True, editable=False, default=uuid4, verbose_name="uuid"
    )
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-updated_time"]
