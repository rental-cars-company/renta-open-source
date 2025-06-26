class UserNoDocuments(Exception):
    """У пользователя не загружены документы."""


class UserWaitsForValidation(Exception):
    """Документы есть. Требуется проверка админов."""


class UserDocumentsRejected(Exception):
    """Документы не прошли проверку. Rejected."""
