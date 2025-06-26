from hashlib import md5

from django.conf import settings
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from api.bookings.models import Booking
from api.payments.models import Card, Payment
from api.payments.serializers import (
    BindCardConfirmResponseSerializer,
    BindCardConfirmSerializer,
    BindCardDialResponseSerializer,
    BindCardDialSerializer,
    BindCardInitResponseSerializer,
    BindCardInitSerializer,
    DepositSerializer,
    ListCardsResponseSerializer,
    ListCardsSerializer,
    PaymentCallbackSerializer,
    PaymentSerializer,
    RemoveCardResponseSerializer,
    RemoveCardSerializer,
    ReversePaymentSerializer,
    TokenHoldSerializer,
    TokenSaleSerializer,
)
from api.payments.services import AtmosClient

client = AtmosClient()


@extend_schema(tags=["Payments"], responses={200: PaymentSerializer(many=True)})
class ListPaymentsAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.is_staff or user.is_superuser:
            qs = Payment.objects.all()
        else:
            qs = Payment.objects.filter(booking__user=user)

        return Response(PaymentSerializer(qs, many=True).data)


@extend_schema(tags=["Payments"], responses={200: PaymentSerializer})
class RetrievePaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        if user.is_staff or user.is_superuser:
            p = get_object_or_404(Payment, pk=pk)
        else:
            p = get_object_or_404(Payment, pk=pk, booking__user=user)
        return Response(PaymentSerializer(p).data)


@extend_schema(
    tags=["Payments"],
    request=TokenSaleSerializer,
    responses={
        201: PaymentSerializer,
        402: OpenApiResponse(description="Недостаточно средств на балансе"),
    },
)
@extend_schema(
    tags=["Payments"],
    request=TokenSaleSerializer,
    responses={
        201: PaymentSerializer,
        402: OpenApiResponse(description="Недостаточно средств на балансе"),
    },
)
class CreateSaleAPIView(APIView):
    """Одношаговый SALE по привязанной карте или CASH."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = TokenSaleSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        booking = get_object_or_404(
            Booking, pk=data["booking_id"], user=request.user
        )
        summary = booking.rental_summary
        amount = int((summary["total_price"] - summary["deposit"]) * 100)

        # --- CASH ---
        if data["method"] == Payment.Method.CASH:
            payment = Payment.objects.create(
                booking=booking,
                method=Payment.Method.CASH,
                sale_amount=amount,
                status=Payment.Status.SUCCESS,
            )
            booking.payment_method = Payment.Method.CASH
            booking.status = Booking.Status.ACCEPTED
            booking.save(update_fields=["payment_method", "status"])
            return Response(
                PaymentSerializer(payment).data, status=status.HTTP_201_CREATED
            )

        # --- CARD ---
        card = get_object_or_404(  # noqa: F841
            Card, card_token=data["card_token"], user=request.user
        )

        # выполнение транзакции SALE через ATMOS
        resp = client.pay_with_token(
            amount=amount,
            account=str(booking.pk),
            store_id=settings.ATMOS_STORE_ID,
            card_token=data["card_token"],
            terminal_id=data.get("terminal_id"),
            lang=data.get("lang", "ru"),
        )

        # Обработка ошибки платёжки
        if resp.get("status") == "error":
            error_msg = resp.get("message", "Ошибка оплаты")
            return Response(
                {"detail": error_msg},
                status=status.HTTP_402_PAYMENT_REQUIRED,
            )

        payment = Payment.objects.create(
            booking=booking,
            method=Payment.Method.CARD,
            sale_transaction_id=resp["transaction_id"],
            sale_success_id=resp.get("store_transaction", {}).get(
                "success_trans_id"
            ),
            sale_amount=amount,
            status=Payment.Status.SUCCESS,
        )
        booking.payment_method = Payment.Method.CARD
        booking.status = Booking.Status.ACCEPTED
        booking.save(update_fields=["payment_method", "status"])
        return Response(
            PaymentSerializer(payment).data, status=status.HTTP_201_CREATED
        )


@extend_schema(
    tags=["Payments"],
    request=TokenHoldSerializer,
    responses={
        201: PaymentSerializer,
        402: OpenApiResponse(description="Недостаточно средств на балансе"),
    },
)
class CreateHoldAPIView(APIView):
    """Единошаговый HOLD по карте (CARD) или наличными (CASH)."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = TokenHoldSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        booking = get_object_or_404(
            Booking, pk=data["booking_id"], user=request.user
        )
        summary = booking.rental_summary
        deposit = summary.get("deposit", 0)
        amount = int(deposit * 100)

        # --- CASH ---
        if data["method"] == Payment.Method.CASH:
            payment = Payment.objects.create(
                booking=booking,
                method=Payment.Method.CASH,
                deposit_amount=amount,
                status=Payment.Status.SUCCESS,
                hold_status=Payment.HoldStatus.AUTHORIZED,
            )
            booking.payment_method = Payment.Method.CASH
            booking.status = Booking.Status.ACCEPTED
            booking.save(update_fields=["payment_method", "status"])
            return Response(
                PaymentSerializer(payment).data, status=status.HTTP_201_CREATED
            )

        # --- ZERO DEPOSIT ---
        if amount == 0:
            payment = Payment.objects.create(
                booking=booking,
                method=Payment.Method.CARD,
                deposit_amount=0,
                status=Payment.Status.SUCCESS,
                hold_status=Payment.HoldStatus.AUTHORIZED,
            )
            booking.payment_method = Payment.Method.CARD
            booking.save(update_fields=["payment_method"])
            return Response(
                PaymentSerializer(payment).data, status=status.HTTP_200_OK
            )

        # --- CARD ---
        card = get_object_or_404(  # noqa: F841
            Card, card_token=data["card_token"], user=request.user
        )

        # выполнение транзакции HOLD через ATMOS
        resp = client.hold_with_token(
            store_id=settings.ATMOS_STORE_ID,
            account=str(booking.pk),
            amount=amount,
            duration=7 * 24 * 60,
            card_token=data["card_token"],
            payment_details=data.get("payment_details", ""),
        )

        # Обработка ошибки платёжки
        if resp.get("status") == "error":
            error_msg = resp.get("message", "Ошибка оплаты")
            return Response(
                {"detail": error_msg},
                status=status.HTTP_402_PAYMENT_REQUIRED,
            )

        payment = Payment.objects.create(
            booking=booking,
            method=Payment.Method.CARD,
            status=Payment.Status.PENDING,
            hold_transaction_id=resp["hold_id"],
            hold_success_id=resp.get("success_trans_id", resp["hold_id"]),
            deposit_amount=amount,
            hold_status=Payment.HoldStatus.AUTHORIZED,
        )
        booking.payment_method = Payment.Method.CARD
        booking.save(update_fields=["payment_method"])
        return Response(
            PaymentSerializer(payment).data, status=status.HTTP_201_CREATED
        )


@extend_schema(
    tags=["Payments"],
    request=PaymentCallbackSerializer,
    responses={200: OpenApiResponse(description="Callback response")},
)
class CallbackAPIView(APIView):
    """POST /api/payments/callback/."""

    permission_classes = []

    def post(self, request):
        ser = PaymentCallbackSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        d = ser.validated_data

        raw = f"{d['store_id']}{d['transaction_id']}{d['invoice']}{d['amount']}{settings.ATMOS_CONSUMER_SECRET}"
        if md5(raw.encode()).hexdigest() != d["sign"]:
            return Response(
                {"status": 0, "message": "Invalid sign"},
                status=status.HTTP_403_FORBIDDEN,
            )

        p = Payment.objects.filter(
            sale_transaction_id=d["transaction_id"]
        ).first()
        if not p:
            return Response(
                {"status": 0, "message": "Payment not found"},
                status=status.HTTP_200_OK,
            )

        p.status = Payment.Status.SUCCESS
        p.atm_invoice = d["invoice"]
        p.request_sign = d["sign"]
        p.save(update_fields=["status", "atm_invoice", "request_sign"])
        return Response({"status": 1, "message": "Успешно"})


# === Card Binding ===


@extend_schema(
    tags=["Payments"],
    request=BindCardInitSerializer,
    responses={200: BindCardInitResponseSerializer},
)
class BindCardInitAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = BindCardInitSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        resp = client.bind_card_init(
            card_number=ser.validated_data["card_number"],
            expiry=ser.validated_data["expiry"],
        )
        return Response(resp)


@extend_schema(
    tags=["Payments"],
    request=BindCardConfirmSerializer,
    responses={200: BindCardConfirmResponseSerializer},
)
class BindCardConfirmAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = BindCardConfirmSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        resp = client.bind_card_confirm(
            transaction_id=ser.validated_data["transaction_id"],
            otp=ser.validated_data["otp"],
        )

        data = resp.get("data", {})
        Card.objects.update_or_create(
            user=request.user,
            card_id=data.get("card_id"),
            defaults={
                "card_token": data.get("card_token"),
                "pan": data.get("pan"),
                "expiry": data.get("expiry"),
                "card_holder": data.get("card_holder", ""),
                "balance": data.get("balance"),
                "card_phone": data.get("phone", ""),
            },
        )

        return Response(resp)


@extend_schema(
    tags=["Payments"],
    request=BindCardDialSerializer,
    responses={200: BindCardDialResponseSerializer},
)
class BindCardDialAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        ser = BindCardDialSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        resp = client.bind_card_dial(
            transaction_id=ser.validated_data["transaction_id"]
        )
        return Response(resp)


@extend_schema(
    tags=["Payments"],
    request=ListCardsSerializer,
    responses={200: ListCardsResponseSerializer},
)
class ListCardsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = ListCardsSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        resp = client.list_cards(
            page=ser.validated_data["page"],
            page_size=ser.validated_data["page_size"],
        )
        return Response(resp)


@extend_schema(
    tags=["Payments"],
    request=RemoveCardSerializer,
    responses={200: RemoveCardResponseSerializer},
)
class RemoveCardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = RemoveCardSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        resp = client.remove_card(
            id=ser.validated_data["id"], token=ser.validated_data["token"]
        )
        # очистим модель от удалённой карты
        Payment.objects.filter(card_id=ser.validated_data["id"]).update(
            card_id=None,
            card_token=None,
            pan=None,
            expiry=None,
            card_holder=None,
            card_balance=None,
            card_phone=None,
        )
        return Response(resp)


@extend_schema(
    tags=["Payments"],
    request=ReversePaymentSerializer,
    responses={200: PaymentSerializer},
)
class ReversePaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = ReversePaymentSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        payment = get_object_or_404(
            Payment,
            sale_success_id=data["transaction_id"],
            booking__user=request.user,
        )

        resp = client.reverse(
            transaction_id=data["transaction_id"],
            reason=data.get("reason"),
            hold_amount=data.get("hold_amount"),
        )

        payment.status = Payment.Status.CANCELLED
        payment.reverse_transaction_id = resp.get("transaction_id")
        payment.reverse_response = resp.get("result")
        payment.save(
            update_fields=[
                "status",
                "reverse_transaction_id",
                "reverse_response",
            ]
        )

        return Response(
            PaymentSerializer(payment).data, status=status.HTTP_200_OK
        )


@extend_schema(
    tags=["Payments"], request=None, responses={200: PaymentSerializer}
)
class HoldDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        # Capture: списание захолдированной суммы
        if request.user.is_superuser or request.user.is_staff:
            payment = get_object_or_404(Payment, hold_transaction_id=id)
        else:
            payment = get_object_or_404(
                Payment, hold_transaction_id=id, booking__user=request.user
            )

        resp = client.hold_capture(id)
        store_tx = resp.get("store_transaction", {})
        payment.hold_success_id = store_tx.get(
            "success_trans_id", payment.hold_success_id
        )
        payment.hold_status = Payment.HoldStatus.CAPTURED
        payment.status = Payment.Status.SUCCESS
        payment.save(update_fields=["hold_success_id", "hold_status", "status"])
        return Response(
            PaymentSerializer(payment).data, status=status.HTTP_200_OK
        )

    def delete(self, request, id):
        # Release: отмена холда
        if request.user.is_superuser or request.user.is_staff:
            payment = get_object_or_404(Payment, hold_transaction_id=id)
        else:
            payment = get_object_or_404(
                Payment, hold_transaction_id=id, booking__user=request.user
            )

        resp = client.hold_cancel(id)  # noqa: F841
        payment.hold_status = Payment.HoldStatus.RELEASED
        payment.status = Payment.Status.CANCELLED
        payment.save(update_fields=["hold_status", "status"])
        return Response(
            PaymentSerializer(payment).data, status=status.HTTP_200_OK
        )


class WalletAPIView(APIView):
    """GET /api/payments/wallet/
    Возвращает последний захолдированный депозит для текущего пользователя.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Payments"], request=None, responses={200: DepositSerializer}
    )
    def get(self, request):
        # находим для пользователя самый последний холд со статусом AUTHORIZED
        last_hold = (
            Payment.objects.filter(
                booking__user=request.user,
                hold_status=Payment.HoldStatus.AUTHORIZED,
            )
            .order_by("-created_time")
            .first()
        )
        deposit_tyiyn = last_hold.deposit_amount if last_hold else 0
        deposit = deposit_tyiyn / 100
        return Response({"deposit": deposit})
