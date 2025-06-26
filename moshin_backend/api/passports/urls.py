from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.passports.views import (
    NewPassportCreateView,
    OldPassportCreateView,
    PassportViewSet,
)

router = DefaultRouter()
router.register(r"", PassportViewSet, basename="driverlicenses")

urlpatterns = [
    path("old/", OldPassportCreateView.as_view()),
    path("new/", NewPassportCreateView.as_view()),
    path("", include(router.urls)),
]
