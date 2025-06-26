from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.locations.views import LocationViewSet

router = DefaultRouter()

router.register(r"", LocationViewSet, basename="location")

urlpatterns = [
    path("", include(router.urls)),
]
