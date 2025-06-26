from rest_framework import serializers

from api.driverlicenses.serializers import DriverLicenseBaseSerializer
from api.passports.serializers import PassportBaseSerializer
from api.referral.serializers import ReferralInfoSerializer
from api.users.models import User
from api.users.services import user_read


class UserSerializer(serializers.ModelSerializer):
    passport = PassportBaseSerializer(read_only=True)
    driverlicense = DriverLicenseBaseSerializer(read_only=True)
    referral = ReferralInfoSerializer(read_only=True)

    validation_status = serializers.SerializerMethodField()

    def get_validation_status(self, obj: User) -> str:
        return user_read.verification_status(obj)

    booking_count = serializers.SerializerMethodField()

    def get_booking_count(self, obj: User) -> int:
        return user_read.bookings_count(obj)

    class Meta:
        depth = 1
        model = User
        fields = (
            # readonly
            "id",
            "role",
            "username",
            "phone",
            "referral",
            # writable
            "name",
            "surname",
            "profile_image",
            # methods
            "validation_status",
            "booking_count",
            "age",
            # documents
            "driverlicense",
            "passport",
        )
        read_only_fields = (
            "id",
            "role",
            "username",
            "phone",
            "referral",
            # methods
            "validation_status",
            "booking_count",
            "age",
            # documents
            "driverlicense",
            "passport",
        )
