from django.urls import path
from rest_framework.routers import DefaultRouter

from api.users.views import (
    CheckPhoneRegisterdView,
    CredentialsRegisterView,
    GetMyUser,
    SetLanguageView,
    UpdateFCMTokenView,
    UserViewSet,
)

router = DefaultRouter()
router.register(r"", UserViewSet, basename="users")


urlpatterns = [
    path("language/", SetLanguageView.as_view()),
    path(
        "admin/", CredentialsRegisterView.as_view(), name="credentials-register"
    ),
    path("fcm-token/", UpdateFCMTokenView.as_view(), name="update-fcm-token"),
    path(
        "is-registered/",
        CheckPhoneRegisterdView.as_view(),
        name="check-registered",
    ),
    path("get-my/", GetMyUser.as_view()),
]
urlpatterns += router.urls
