from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView, TokenVerifyView

from .views import (
    LoginWithCredentialsView,
    LoginWithPhoneView,
    RenterLoginRegisterView,
    TokenRefreshView,
)

urlpatterns = [
    path(
        "login/admin/",
        LoginWithCredentialsView.as_view(),
        name="token_obtain_pair_credentials",
    ),
    path(
        "login/renter/",
        LoginWithPhoneView.as_view(),
        name="token_obtain_pair_renter",
    ),
    path(
        "register-login/renter/",
        RenterLoginRegisterView.as_view(),
        name="renter_login_register",
    ),
    path("token-refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token-verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("logout/", TokenBlacklistView.as_view(), name="token_logout"),
]
