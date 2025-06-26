from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from api.payments.models import Payment
from api.payments.services import AtmosClient


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "booking",
        "payment_method_display",
        "sale_amount_display",
        "deposit_amount_display",
        "status",
        "hold_status",
        "sale_transaction_id",
        "sale_success_id",
        "hold_transaction_id",
        "hold_success_id",
        "hold_release_date",
        "atm_invoice",
        "request_sign",
        "created_time",
    )
    list_filter = ("status", "hold_status", "method", "created_time")
    search_fields = (
        "sale_transaction_id",
        "hold_transaction_id",
        "booking__user__phone",
    )
    readonly_fields = (
        "sale_transaction_id",
        "sale_success_id",
        "sale_amount",
        "hold_transaction_id",
        "hold_success_id",
        "deposit_amount",
        "hold_status",
        "hold_release_date",
        "atm_invoice",
        "request_sign",
        "created_time",
        "updated_time",
    )
    actions = ["capture_holds", "release_holds"]

    @admin.display(description=_("Метод оплаты"))
    def payment_method_display(self, obj):
        return obj.get_method_display()

    @admin.display(description=_("Сумма аренды"))
    def sale_amount_display(self, obj):
        if obj.sale_amount is not None:
            return f"{obj.sale_amount / 100:.2f} UZS"
        summary = obj.booking.rental_summary
        return f"{summary.get('rental_cost', 0):.2f} UZS"

    @admin.display(description=_("Сумма залога"))
    def deposit_amount_display(self, obj):
        if obj.deposit_amount is not None:
            return f"{obj.deposit_amount / 100:.2f} UZS"
        summary = obj.booking.rental_summary
        return f"{summary.get('deposit', 0):.2f} UZS"

    @admin.action(description=_("Списать депозит для выделенных"))
    def capture_holds(self, request, queryset):
        client = AtmosClient()
        updated = 0
        for p in queryset.filter(
            hold_transaction_id__isnull=False,
            hold_status=Payment.HoldStatus.AUTHORIZED,
        ):
            client.hold_capture(p.hold_transaction_id)
            p.hold_success_id = p.hold_transaction_id
            p.hold_status = Payment.HoldStatus.CAPTURED
            p.save(update_fields=["hold_success_id", "hold_status"])
            updated += 1
        self.message_user(request, _(f"Депозиты списаны: {updated}"))

    @admin.action(description=_("Вернуть депозит для выделенных"))
    def release_holds(self, request, queryset):
        client = AtmosClient()
        updated = 0
        for p in queryset.filter(hold_transaction_id__isnull=False).exclude(
            hold_status=Payment.HoldStatus.RELEASED
        ):
            client.hold_cancel(p.hold_transaction_id)
            p.hold_status = Payment.HoldStatus.RELEASED
            p.save(update_fields=["hold_status"])
            updated += 1
        self.message_user(request, _(f"Депозиты возвращены: {updated}"))

    def save_model(self, request, obj, form, change):
        # Подставляем суммы из расчёта rental_summary
        summary = obj.booking.rental_summary
        if obj.sale_amount is None:
            obj.sale_amount = int(summary.get("rental_cost", 0) * 100)
        if obj.deposit_amount is None:
            obj.deposit_amount = int(summary.get("deposit", 0) * 100)
        super().save_model(request, obj, form, change)
