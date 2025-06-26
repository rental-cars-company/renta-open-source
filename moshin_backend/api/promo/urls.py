from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.promo.views import CouponViewSet, GetCouponIdByNameView

router = DefaultRouter()
router.register(r"", CouponViewSet, basename="coupons")

urlpatterns = [
    path("check/", GetCouponIdByNameView.as_view()),
    path("", include(router.urls)),
]
