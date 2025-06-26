from django.urls import path
from api.payments.views import (
    ListPaymentsAPIView,
    RetrievePaymentAPIView,
    CreateSaleAPIView,
    CreateHoldAPIView,
    CallbackAPIView,
    BindCardInitAPIView,
    BindCardConfirmAPIView,
    BindCardDialAPIView,
    ListCardsAPIView,
    RemoveCardAPIView,
    ReversePaymentAPIView,
    HoldDetailAPIView,
    WalletAPIView,
)

app_name = "payments"

urlpatterns = [
    # Локальные эндпоинты (просмотр собственных платежей)
    path("",                 ListPaymentsAPIView.as_view(), name="list"),
    path("<uuid:pk>/",       RetrievePaymentAPIView.as_view(), name="retrieve"),

    # Sale — едино-шаговая оплата по привязанной карте
    path("merchant/pay/create/", CreateSaleAPIView.as_view(), name="sale-create"),

    # Hold — едино-шаговый холд по привязанной карте
    path("hold/create/",      CreateHoldAPIView.as_view(),    name="hold-create"),
    path("hold/<int:id>/", HoldDetailAPIView.as_view(), name="hold-detail"),

    # Callback от ATMOS
    path("callback/",         CallbackAPIView.as_view(),      name="callback"),

    # Card binding — ATMOS API
    path("partner/bind-card/init/",    BindCardInitAPIView.as_view(),    name="bind-card-init"),
    path("partner/bind-card/confirm/", BindCardConfirmAPIView.as_view(), name="bind-card-confirm"),
    path("partner/bind-card/dial/",    BindCardDialAPIView.as_view(),    name="bind-card-dial"),
    path("partner/list-cards/",        ListCardsAPIView.as_view(),       name="list-cards"),
    path("partner/remove-card/",       RemoveCardAPIView.as_view(),     name="remove-card"),

    # Списание и возврат
    path('reverse/', ReversePaymentAPIView.as_view(), name='reverse-payment'),

    # Wallet
    path("wallet/", WalletAPIView.as_view(), name="wallet"),


]
