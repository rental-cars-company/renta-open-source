from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

# Все маршруты, зависящие от языка — внутрь i18n_patterns
urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("api/cars/", include("api.cars.urls")),
    path("api/users/", include("api.users.urls")),
    path("api/auth/", include("api.authentication.urls")),
    path("api/bookings/", include("api.bookings.urls")),
    path("api/locations/", include("api.locations.urls")),
    path("api/passports/", include("api.passports.urls")),
    path("api/driverlicenses/", include("api.driverlicenses.urls")),
    path("api/payments/", include("api.payments.urls", namespace="payments")),
    path("api/notifications/", include("api.notifications.urls")),
    path("api/coupons/", include("api.promo.urls")),
    path("api/referral/", include("api.referral.urls")),
    path("api/version_control/", include("api.version_control.urls")),
    prefix_default_language=True,
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
