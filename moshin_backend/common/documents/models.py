from django.db import models
from django.utils.translation import gettext_lazy as _

from common.documents.constants import (
    DOCUMENT_PENDING,
    DOCUMENT_VALIDATION_STATUS_CHOICES,
)
from common.models import ModelBase


class DocumentBase(ModelBase):
    class Meta(ModelBase.Meta):
        abstract = True

    validation_status = models.CharField(
        verbose_name=_("Состояние валидации"),
        choices=DOCUMENT_VALIDATION_STATUS_CHOICES,
        default=DOCUMENT_PENDING,
    )
