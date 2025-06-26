from django.utils.translation import gettext_lazy as _


class ReadingDocumentError(Exception):
    default_message: str = _("Ошибка чтения документа")

    def __init__(self, message: str | None = None):
        if message is None:
            message = self.__class__.default_message
        self.message: str = message
