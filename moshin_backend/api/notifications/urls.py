from rest_framework.routers import DefaultRouter

from api.notifications.views import DeviceViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r"devices", DeviceViewSet, basename="devices")
router.register(r"", NotificationViewSet, basename="notifications")

urlpatterns = router.urls
