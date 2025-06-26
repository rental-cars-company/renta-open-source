from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from decimal import Decimal

from api.bookings.models import Booking, BookingStatusLog

from .forms import BookingAdminForm


class BookingResource(resources.ModelResource):
    class Meta:
        model = Booking
        fields = (
            "id",
            "user__name",
            "user__phone",
            "car__brand",
            "car__model",
            "car__fleet__name",
            "start_datetime",
            "end_datetime",
            "delivery_option",
            "status",
            "total_price",
            "created_time",
            "updated_time",
        )


class BookingStatusLogResource(resources.ModelResource):
    class Meta:
        model = BookingStatusLog
        fields = (
            "booking__id",
            "booking__user__name",
            "booking__car__model",
            "old_status",
            "new_status",
            "changed_by__username",
            "changed_at",
        )


@admin.register(Booking)
class BookingAdmin(ImportExportActionModelAdmin):
    resource_classes = [BookingResource]
    form = BookingAdminForm
    list_display = (
        "id",
        "created_time",
        "user_name",
        "car_name",
        "rental_company",
        "booking_dates",
        "delivery_info",
        "deposit",
        "status",
        "payment_type",
        "total_price",
        "deposit_status",
        "passport_preview",
        "license_preview",
        "driver_requested",
        "action_buttons",
    )
    list_filter = ("status", "delivery_option", "created_time", "user", "car")
    search_fields = ("user__name", "user__phone", "car__model", "car__brand")
    ordering = ("-created_time",)
    readonly_fields = (
        "created_time",
        "updated_time",
        "passport_preview",
        "license_preview",
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "change-status/<uuid:booking_id>/<str:new_status>/",
                self.admin_site.admin_view(self.change_status),
                name="booking-change-status",
            )
        ]
        return custom_urls + urls

    def change_status(self, request, booking_id, new_status):
        obj = Booking.objects.get(pk=booking_id)
        old_status = obj.status
        obj.status = new_status
        obj.save()
        BookingStatusLog.objects.create(
            booking=obj,
            old_status=old_status,
            new_status=new_status,
            changed_by=request.user,
        )
        self.message_user(
            request,
            _("Статус обновлён: %(old)s → %(new)s")
            % {"old": old_status, "new": new_status},
            messages.SUCCESS,
        )
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    def action_buttons(self, obj):
        buttons = []
        transitions = {
            "pending": ["on_process", "cancelled"],
            "on_process": ["on_delivery", "cancelled"],
            "on_delivery": ["accepted", "cancelled"],
            "accepted": ["finished"],
        }
        next_steps = transitions.get(obj.status, [])
        for status in next_steps:
            url = reverse("admin:booking-change-status", args=[obj.id, status])
            color = (
                "green"
                if status == "finished"
                else "orange" if status == "accepted" else "gray"
            )
            buttons.append(
                f'<a class="button" style="margin-right:5px; color:white; background-color:{color}; padding:3px 8px; border-radius:4px" '
                f'href="{url}">→ {status.replace("_", " ").title()}</a>'
            )
        return format_html(" ".join(buttons))

    @admin.display(description=_("Имя пользователя"))
    def user_name(self, obj):
        if obj.user.name:
            return obj.user.name
        if obj.user.surname:
            return f"{obj.user.surname} {obj.user.name or ''}".strip()
        return obj.user.phone or obj.user.username

    @admin.display(description=_("Машина"))
    def car_name(self, obj):
        return f"{obj.car.brand} {obj.car.model}"

    @admin.display(description=_("Арендная компания"))
    def rental_company(self, obj):
        return (
            obj.car.fleet.name if obj.car.fleet else _("Принадлежит платформе")
        )

    @admin.display(description=_("Даты бронирований"))
    def booking_dates(self, obj):
        return f"{obj.start_datetime.date()} – {obj.end_datetime.date()}"

    @admin.display(description=_("Способ доставки"))
    def delivery_info(self, obj):
        if obj.delivery_option == "delivery":
            return _("Доставить на: [%(lat)s, %(lon)s]") % {
                "lat": obj.delivery_latitude,
                "lon": obj.delivery_longitude,
            }
        return _("Самовывоз")

    @admin.display(description=_("Тип платежа"))
    def payment_type(self, obj):
        p = obj.payments.first()
        if not p:
            return "—"
        return f"{p.get_method_display()} ({p.get_status_display()})"

    @admin.display(description=_("Итоговая цена"))
    def total_price(self, obj):
        return f"{obj.total_price} UZS"

    @admin.display(description=_("Депозит"))
    def deposit(self, obj):
        return obj.deposit

    @admin.display(description=_("Залог (статус)"))
    def deposit_status(self, obj: Booking):
        # 1) Сумма из поля Booking.deposit
        amount = obj.deposit or Decimal("0")

        # 2) Определяем, удержан ли залог по платёжке
        payment = obj.payments.first()
        if payment and payment.keep_deposit:
            status = _("Удержан")
        else:
            status = _("Будет возвращён")

        # 3) Возвращаем строку "сумма — статус"
        return f"{amount} — {status}"

    @admin.display(description=_("Паспорт"))
    def passport_preview(self, obj):
        passport = getattr(obj.user, "passportinfo", None)
        if passport and passport.image_file:
            return format_html(
                '<img src="{}" width="100" />', passport.image_file.url
            )
        return "—"

    @admin.display(description=_("Водительское удостоверение"))
    def license_preview(self, obj):
        license_obj = getattr(obj.user, "driverlicense", None)
        if license_obj and license_obj.image_file:
            return format_html(
                '<img src="{}" width="100" />', license_obj.image_file.url
            )
        return "—"

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("user", "car", "car__fleet")
        )

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = Booking.objects.get(pk=obj.pk)
            if old_obj.status != obj.status:
                BookingStatusLog.objects.create(
                    booking=obj,
                    old_status=old_obj.status,
                    new_status=obj.status,
                    changed_by=request.user,
                )
        super().save_model(request, obj, form, change)


@admin.register(BookingStatusLog)
class BookingStatusLogAdmin(ImportExportActionModelAdmin):
    resource_class = BookingStatusLogResource
    list_display = (
        "booking_id_display",
        "user_phone_display",
        "car_model_display",
        "old_status",
        "new_status",
        "admin_username_display",
        "changed_at",
    )
    list_filter = ("new_status", "changed_by", "changed_at")
    search_fields = (
        "booking__user__phone",
        "booking__user__name",
        "booking__car__model",
        "changed_by__username",
    )

    @admin.display(description=_("ID бронирования"))
    def booking_id_display(self, obj):
        return obj.booking.id

    @admin.display(description=_("Телефон пользователя"))
    def user_phone_display(self, obj):
        return obj.booking.user.phone

    @admin.display(description=_("Автомобиль"))
    def car_model_display(self, obj):
        return obj.booking.car.model

    @admin.display(description=_("Администратор"))
    def admin_username_display(self, obj):
        return obj.changed_by.username if obj.changed_by else "—"
