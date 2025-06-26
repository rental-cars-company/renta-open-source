from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AppVersionViewSet

router = DefaultRouter()
router.register(r"", AppVersionViewSet, basename="app-version")

urlpatterns = [
    path("", include(router.urls)),
]
