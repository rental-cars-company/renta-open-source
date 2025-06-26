from django.utils.translation import gettext_lazy as _

DOCUMENT_PENDING = "pending"
DOCUMENT_EXTRACT_FAILED = "extract_failed"
DOCUMENT_EXTRACT_VERIFIED = "extract_verified"
DOCUMENT_APPROVED = "approved"
DOCUMENT_REJECTED = "rejected"

DOCUMENT_VALIDATION_STATUS_CHOICES = (
    (DOCUMENT_PENDING, _("Ожидание авто проверки")),
    (DOCUMENT_EXTRACT_FAILED, _("Авто проверка не выполнена")),
    (DOCUMENT_EXTRACT_VERIFIED, _("Авто проверка успешна")),
    (DOCUMENT_APPROVED, _("Подтверждено")),
    (DOCUMENT_REJECTED, _("Отклонено")),
)


ALLOWED_DOCUMENT_FILE_EXTENSIONS = (".jpg", ".png", ".pdf")
BLOCK_RENTER_DOCUMENT_PATCH_STATUSES = (DOCUMENT_PENDING, DOCUMENT_APPROVED)
