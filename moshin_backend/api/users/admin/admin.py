from typing import TYPE_CHECKING

from django.contrib import admin
from django.db.models import Count
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _

from api.bookings.models import Booking
from api.referral.services import referral_service
from api.users.admin.forms import UserAdminForm
from api.users.models import User
from api.users.services import user_read

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.http import HttpRequest


@admin.action(description=_("Добавить реферальные данные"))
def create_ref_balance(
    modeladmin, request: "HttpRequest", queryset: "QuerySet"
):
    qs = queryset.select_related("referral").filter(referral=None)
    for user in qs.all():
        referral_service.register(user, referral_code=None)


class BookingCountFilter(admin.SimpleListFilter):
    title = _("Количество бронирований")
    parameter_name = "has_bookings"

    def lookups(self, request: "HttpRequest", model_admin):
        return (
            ("0", _("0 бронирований")),
            ("1+", _("Хотя бы 1 бронирование")),
        )

    def queryset(self, request: "HttpRequest", queryset: "QuerySet"):
        qs = queryset.annotate(bookings_count=Count("bookings"))
        if self.value() == "0":
            return qs.filter(bookings_count=0)
        if self.value() == "1+":
            return qs.filter(bookings_count__gte=1)
        return queryset


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    actions = [create_ref_balance]
    list_display = (
        "id",
        "account",
        "name",
        "surname",
        "age",
        "verification_status",
        "bookings_count",
        "referral_invites",
        "referral_balance",
    )

    readonly_fields = (
        "verification_status",
        "bookings_count",
        "referral_invites",
        "referral_balance",
    )

    list_filter = (
        "driverlicense__validation_status",
        "age",
        BookingCountFilter,
    )

    search_fields = (
        "name",
        "surname",
        "phone",
    )

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "role",
                    "language",
                    "name",
                    "surname",
                    "age",
                ),
            },
        ),
        (
            "Readonly",
            {
                "fields": (
                    "verification_status",
                    "bookings_count",
                    "referral_invites",
                    "referral_balance",
                ),
            },
        ),
        (
            "Credentials",
            {
                "classes": ["collapse"],
                "fields": ("username", "password"),
            },
        ),
        (
            "Renter",
            {
                "classes": ["collapse"],
                "fields": ("phone",),
            },
        ),
    ]

    def get_queryset(self, request: "HttpRequest") -> "QuerySet":
        return user_read.get_queryset()

    @admin.display(description=_("Аккаунт"))
    def account(self, obj):
        return str(obj)

    @admin.display(description=_("Статус верификации"))
    def verification_status(self, obj):
        try:
            return obj.driverlicense.validation_status
        except obj.driverlicense.RelatedObjectDoesNotExist:
            return False

    @admin.display(description=_("Количество бронирований"))
    def bookings_count(self, obj):
        return Booking.objects.filter(user=obj).count()

    # referral
    @admin.display(description=_("Число приглашенных пользователей"))
    def referral_invites(self, obj):
        try:
            return obj.referral.users_invited
        except obj.__class__.referral.RelatedObjectDoesNotExist:
            return 0

    @admin.display(description=_("Реферальный баланс"))
    def referral_balance(self, obj):
        try:
            return obj.referral.balance
        except obj.__class__.referral.RelatedObjectDoesNotExist:
            return 0

    # --
