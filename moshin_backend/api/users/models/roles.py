from django.utils.translation import gettext_lazy as _

USER_ROLE_CHOICES = [
    ("renter", _("Пользователь")),
    ("admin", _("Администратор")),
    ("superuser", _("Суперпользователь")),
]
USER_ROLE_ADMIN = "admin"
USER_ROLE_RENTER = "renter"
USER_ROLE_SUPERUSER = "superuser"
