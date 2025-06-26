from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.driverlicenses.views import (
    DriverLicenseCreateView,
    DriverLicenseViewSet,
)

router = DefaultRouter()
router.register(r"", DriverLicenseViewSet, basename="driverlicenses")

urlpatterns = [
    path("", DriverLicenseCreateView.as_view()),
    path("", include(router.urls)),
]
