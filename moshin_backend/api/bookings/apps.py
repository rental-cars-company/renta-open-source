from django.apps import AppConfig


class BookingsConfig(AppConfig):
    name = "api.bookings"

    def ready(self):
        import api.bookings.signals
