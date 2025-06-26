from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

from .roles import USER_ROLE_SUPERUSER


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError(_("У пользователя должен быть номер телефона"))

        extra_fields.setdefault("username", phone)  # чтобы не вызывало ошибок
        user = self.model(phone=phone, **extra_fields)
        if password is not None:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", USER_ROLE_SUPERUSER)
        extra_fields.setdefault("username", username)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Суперпользователь должен иметь is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                _("Суперпользователь должен иметь is_superuser=True.")
            )

        return self.create_user(
            phone=username, password=password, **extra_fields
        )
