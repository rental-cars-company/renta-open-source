import decimal

from django.utils.translation import gettext_lazy as _

# Координаты города для брони
TASHKENT_LAT_MIN = 41.0
TASHKENT_LAT_MAX = 41.4
TASHKENT_LONG_MIN = 69.0
TASHKENT_LONG_MAX = 69.5

# Способ доставки
DELIVERY_OPTIONS = [("pickup", _("Самовывоз")), ("delivery", _("Доставка"))]
DELIVERY_OPTION_DELIVERY = "delivery"
DELIVERY_PRICE = 50000
RETURN_PICKUP_PRICE = 50000
DRIVER_PRICE_PER_DAY = 300000

CAR_CLASS_CHOICES = [
    ("standard", _("Стандарт")),
    ("premium", _("Премиум")),
]
CARS_MIN_YEAR = 2010

ENGINE_TYPE_CHOICES = [
    ("electric", _("Электрическая")),
    ("gasoline", _("Бензиновая")),
    ("hybrid", _("Гибридная")),
]

CAR_COLOR_CHOICES = [
    ("white", _("Белый")),
    ("black", _("Чёрный")),
    ("silver", _("Серебристый")),
    ("gray", _("Серый")),
    ("blue", _("Синий")),
    ("red", _("Красный")),
    ("green", _("Зелёный")),
    ("yellow", _("Жёлтый")),
    ("brown", _("Коричневый")),
    ("orange", _("Оранжевый")),
    ("beige", _("Бежевый")),
    ("gold", _("Золотистый")),
    ("purple", _("Фиолетовый")),
    ("other", _("Другой")),
]

CAR_TYPE_CHOICES = [
    ("hatchback", _("Хэтчбек")),
    ("sedan", _("Седан")),
    ("suv", _("Внедорожник")),
    ("mid_suv", _("Mid-size SUV")),
    ("crossover", _("Кроссовер")),
    ("muv", _("Минивэн")),
    ("coupe", _("Купе")),
    ("convertible", _("Кабриолет")),
    ("pickup", _("Пикап")),
]

# Superuser
DO_CREATE_SUPERUSER_ON_START: bool = True
SUPERUSER_PHONE: str = "+998903356990"
SUPERUSER_PASSWORD: str = "superuser"


# permission view action
class action:
    CREATE = "create"
    RETRIEVE = "retrieve"
    LIST = "list"
    DELETE = "destroy"
    PUT = "update"
    PATCH = "partial_update"


#
MINIMUN_AGE_FOR_REGISTER = 18


DECIMAL_MAX_DIGITS = 12
DECIMAL_PLACES = 2
DECIMAL_QUANTIZER = decimal.Decimal(10) ** -DECIMAL_PLACES


#
PASSPORTS_MEDIA_DIR = "passport_images/"
DRIVERLICENSES_MEDIA_DIR = "driverlicense_images/"
USER_PROFILE_MEDIA_DIR = "profile_images/"


# Payments
PAYMENT_METHOD_CARD = "CARD"
PAYMENT_METHOD_CASH = "CASH"

PAYMENT_METHOD_CHOICES = [
    (PAYMENT_METHOD_CARD, _("Карта")),
    (PAYMENT_METHOD_CASH, _("Наличные")),
]


# Caches
CACHE_TIMEOUT = 300


# REFFERAL
BALANCE_FOR_NEW_REFERRAL = 50_000
BALANCE_FOR_REGISTER_AS_REFERRAL = 50_000
