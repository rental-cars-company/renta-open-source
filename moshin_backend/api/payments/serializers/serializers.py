from rest_framework import serializers
from django.shortcuts import get_object_or_404
from api.payments.models import Payment
from api.bookings.models import Booking


class TokenSaleSerializer(serializers.Serializer):
    """
    Одношаговый SALE: либо CARD (по token), либо CASH (по booking_id и method).
    """
    booking_id  = serializers.UUIDField()
    method      = serializers.ChoiceField(
        choices=Payment.Method.choices,
        default=Payment.Method.CARD
    )
    card_token  = serializers.CharField(required=False, allow_blank=True)
    lang        = serializers.ChoiceField(
        choices=[("uz", "uz"), ("ru", "ru"), ("en", "en")],
        default="ru",
        required=False
    )
    terminal_id = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        # проверяем, что бронирование существует
        get_object_or_404(Booking, pk=attrs["booking_id"])
        if attrs["method"] == Payment.Method.CARD:
            #
            if not attrs.get("card_token"):
                raise serializers.ValidationError({
                    "card_token": "При method == CARD обязательно передайте card_token."
                })
        return attrs


class TokenHoldSerializer(serializers.Serializer):
    """
    HOLD по привязанной карте (CARD) или наличными (CASH):
    – booking_id
    – method      (CARD или CASH)
    – card_token  (если CARD)
    – payment_details (опционально)
    """
    booking_id      = serializers.UUIDField()
    method          = serializers.ChoiceField(
        choices=Payment.Method.choices,
        default=Payment.Method.CARD
    )
    card_token      = serializers.CharField(required=False, allow_blank=True)
    payment_details = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        get_object_or_404(Booking, pk=attrs["booking_id"])
        if attrs["method"] == Payment.Method.CARD:
            if not attrs.get("card_token"):
                raise serializers.ValidationError({
                    "card_token": "При method == CARD обязательно передайте card_token."
                })
        # при CASH токен игнорируется
        return attrs

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = [
            'sale_transaction_id', 'sale_success_id', 'sale_amount',
            'hold_transaction_id', 'hold_success_id', 'deposit_amount',
            'hold_status', 'hold_release_date', 'atm_invoice', 'request_sign',
            'created_time', 'updated_time', 'reverse_transaction_id', 'reverse_response',
        ]



class PaymentCallbackSerializer(serializers.Serializer):
    store_id         = serializers.CharField()
    transaction_id   = serializers.IntegerField()
    transaction_time = serializers.DateTimeField()
    amount           = serializers.CharField()
    invoice          = serializers.CharField()
    sign             = serializers.CharField()



# === Card Binding ===

class BindCardInitSerializer(serializers.Serializer):
    card_number = serializers.CharField()
    expiry      = serializers.CharField()


class BindCardInitResponseSerializer(serializers.Serializer):
    result         = serializers.DictField()
    transaction_id = serializers.IntegerField()
    phone          = serializers.CharField()


class BindCardConfirmSerializer(serializers.Serializer):
    transaction_id = serializers.IntegerField()
    otp            = serializers.CharField()


class BindCardConfirmResponseSerializer(serializers.Serializer):
    result = serializers.DictField()
    data   = serializers.DictField()


class BindCardDialSerializer(serializers.Serializer):
    transaction_id = serializers.IntegerField()


class BindCardDialResponseSerializer(serializers.Serializer):
    result = serializers.DictField()


class ListCardsSerializer(serializers.Serializer):
    page      = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)


class CardListItemSerializer(serializers.Serializer):
    card_id    = serializers.IntegerField()
    card_token = serializers.CharField()
    pan        = serializers.CharField()
    expiry     = serializers.CharField()


class ListCardsResponseSerializer(serializers.Serializer):
    result    = serializers.DictField()
    card_list = CardListItemSerializer(many=True)


class RemoveCardSerializer(serializers.Serializer):
    id    = serializers.IntegerField()
    token = serializers.CharField()


class RemoveCardResponseSerializer(serializers.Serializer):
    result = serializers.DictField()
    data   = serializers.DictField()


class ReversePaymentSerializer(serializers.Serializer):
    transaction_id = serializers.IntegerField()
    hold_amount    = serializers.IntegerField(required=False)
    reason         = serializers.CharField(required=False, allow_blank=True)

class DepositSerializer(serializers.Serializer):
    deposit = serializers.IntegerField()