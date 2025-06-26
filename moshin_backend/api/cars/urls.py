from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.cars.views import (
    CarFleetViewSet,
    CarsViewSet,
)

router = DefaultRouter()
router.register(
    r"rental-companies", CarFleetViewSet, basename="rental-companies"
)
router.register(r"", CarsViewSet, basename="cars")

urlpatterns = [
    path("", include(router.urls)),
]
