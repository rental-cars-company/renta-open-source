from django.urls import path
from rest_framework.routers import DefaultRouter

from api.bookings.views import (
    BookingCreateView,
    BookingPriceDetailsView,
    BookingReadViewSet,
    BookingUpdateView,
)

router = DefaultRouter()
router.register(r"", BookingReadViewSet, basename="bookings")

urlpatterns = [
    path("admin-all/", BookingReadViewSet.as_view({"get": "admin_all"})),
    path("my-bookings/", BookingReadViewSet.as_view({"get": "history"})),
    path("details/", BookingPriceDetailsView.as_view()),
    path(
        "<str:pk>/admin-get/", BookingReadViewSet.as_view({"get": "admin_get"})
    ),
    path(
        "<str:pk>/renter-get/", BookingReadViewSet.as_view({"get": "retrieve"})
    ),
    path("<str:pk>/", BookingUpdateView.as_view()),
    path("", BookingCreateView.as_view()),
]
