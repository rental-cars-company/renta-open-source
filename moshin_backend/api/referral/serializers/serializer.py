from rest_framework import serializers

from api.referral.models import ReferralInfo


class ReferralInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralInfo
        fields = (
            "id",
            "own_referral_code",
            "used_referral_code",
            "balance",
            "users_invited",
        )
        read_only_fields = fields
