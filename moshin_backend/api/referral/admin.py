from django.contrib import admin

from api.referral.models import ReferralInfo


@admin.register(ReferralInfo)
class ReferralInfoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "own_referral_code",
        "used_referral_code",
        "balance",
        "users_invited",
    )
