from django.contrib import admin

from api.promo.models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "active", "rental_cost_discount")
