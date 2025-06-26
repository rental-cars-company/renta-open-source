import os
import sentry_sdk
from datetime import timedelta
from pathlib import Path
from django.utils.translation import gettext_lazy as _
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / "dev.env")

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "backend-dev.moshin-rent.uz",
    "api.renta-cars.uz",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

CSRF_TRUSTED_ORIGINS = [
    "https://backend-dev.moshin-rent.uz",
    "https://api.renta-cars.uz",
    "https://panel.renta-cars.uz",
]

INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # external
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "django_filters",
    "import_export",
    "storages",
    # local apps/api
    "core",
    "api.users",
    "api.authentication",
    "api.cars",
    "api.bookings",
    "api.locations",
    "api.passports",
    "api.driverlicenses",
    "api.payments",
    "api.notifications",
    "api.promo",
    "api.validate_uz",
    "api.version_control",
    "api.referral",
    "channels",
]
if DEBUG:
    INSTALLED_APPS.append("silk")

SILKY_IGNORE_PATHS = ["/admin/jsi18n/"]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
if DEBUG:
    MIDDLEWARE.append("silk.middleware.SilkyMiddleware")
SILKY_IGNORE_PATHS = ["/admin/jsi18n/"]


ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [("127.0.0.1", 6379)]},
    }
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "moshin"),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

USE_TZ = True
TIME_ZONE = "Asia/Tashkent"

# ✅ Обновлено
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

APPEND_SLASH = False

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",  # важно для Swagger
    "DEFAULT_PAGINATION_CLASS": "common.pagination.DynamicPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend"
    ],
    "EXCEPTION_HANDLER": "common.exeptions.detailed_exception_handler",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

# Swagger sidecar
SPECTACULAR_SETTINGS = {
    "TITLE": "Moshin API",
    "DESCRIPTION": "Документация для API сервиса аренды автомобилей",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
}

# Cors
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://panel.renta-cars.uz",
]

VERIFICATION_CODE_LENGHT = 6

PAGE_SIZE = 10

# Firebase Cloud Messaging (FCM)
FIREBASE_PROJECT_ID = "moshin-e04e7"
FIREBASE_CREDENTIALS_PATH = os.path.join(
    BASE_DIR, "secrets", "moshin-firebase-key.json"
)

# Redis
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Celery
CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

# ATMOS
ATMOS_STORE_ID = "2172"
ATMOS_CONSUMER_KEY = "k1gq7gjg4W8VgPE1ieALPSu7Rf8a"
ATMOS_CONSUMER_SECRET = "v24xYNf2YQBmhSTGHC58y_YZSTYa"
ATMOS_TOKEN_URL = os.getenv("ATMOS_TOKEN_URL", "https://partner.atmos.uz/token")
ATMOS_CREATE_URL = os.getenv(
    "ATMOS_CREATE_URL", "https://partner.atmos.uz/merchant/pay/create"
)
ATMOS_PREAPPLY_URL = os.getenv(
    "ATMOS_PREAPPLY_URL", "https://partner.atmos.uz/merchant/pay/pre-apply"
)
ATMOS_APPLY_URL = os.getenv(
    "ATMOS_APPLY_URL", "https://partner.atmos.uz/merchant/pay/apply-ofd"
)
ATMOS_REVERSE_URL = os.getenv(
    "ATMOS_REVERSE_URL", "https://partner.atmos.uz/merchant/pay/reverse"
)
ATMOS_GET_URL = os.getenv(
    "ATMOS_GET_URL", "https://partner.atmos.uz/merchant/pay/get"
)
ATMOS_HOLD_CREATE_URL = os.getenv(
    "ATMOS_HOLD_CREATE_URL", "https://partner.atmos.uz/hold/create"
)
ATMOS_HOLD_APPLY_URL = os.getenv(
    "ATMOS_HOLD_APPLY_URL", "https://partner.atmos.uz/hold/apply"
)
ATMOS_HOLD_CAPTURE_URL = os.getenv(
    "ATMOS_HOLD_CAPTURE_URL", "https://partner.atmos.uz/hold"
)
ATMOS_HOLD_CANCEL_URL = os.getenv(
    "ATMOS_HOLD_CANCEL_URL", "https://partner.atmos.uz/hold"
)
ATMOS_HOLD_GET_URL = os.getenv(
    "ATMOS_HOLD_GET_URL", "https://partner.atmos.uz/hold"
)

# ATMOS card-binding endpoints
ATMOS_BIND_INIT_URL = os.getenv(
    "ATMOS_BIND_INIT_URL", "https://partner.atmos.uz/partner/bind-card/init"
)
ATMOS_BIND_CONFIRM_URL = os.getenv(
    "ATMOS_BIND_CONFIRM_URL",
    "https://partner.atmos.uz/partner/bind-card/confirm",
)
ATMOS_BIND_DIAL_URL = os.getenv(
    "ATMOS_BIND_DIAL_URL", "https://partner.atmos.uz/partner/bind-card/dial"
)
ATMOS_LIST_CARDS_URL = os.getenv(
    "ATMOS_LIST_CARDS_URL", "https://partner.atmos.uz/partner/list-cards"
)
ATMOS_REMOVE_CARD_URL = os.getenv(
    "ATMOS_REMOVE_CARD_URL", "https://partner.atmos.uz/partner/remove-card"
)

ATMOS_CALLBACK_IP_WHITELIST = ["185.8.212.47"]

TESSERACT_CMD_PATH = os.environ.get("TESSERACT_CMD_PATH", None)

# ESKIZ
ESKIZ_EMAIL = os.getenv("ESKIZ_EMAIL")
ESKIZ_PASSWORD = os.getenv("ESKIZ_PASSWORD")

# Настройки языка
LANGUAGE_CODE = "ru"  # язык по умолчанию
LANGUAGES = [
    ("uz", _("Uzbek")),
    ("ru", _("Russian")),
    ("en", _("English")),
]
USE_I18N = True
USE_L10N = True
LOCALE_PATHS = [
    BASE_DIR / "locale",  # Папка, где будут храниться переводы
]

# Static Config

STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# AWS S3 settings
AWS_ACCESS_KEY_ID = os.getenv("AWS_S3_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_S3_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

# Object parameters
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}

# S3 Storage settings
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
        "OPTIONS": {
            "access_key": AWS_ACCESS_KEY_ID,
            "secret_key": AWS_SECRET_ACCESS_KEY,
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "region_name": AWS_S3_REGION_NAME,
            "custom_domain": AWS_S3_CUSTOM_DOMAIN,
            "default_acl": None,
            "querystring_auth": False,
            "location": "media",
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
        "OPTIONS": {
            "access_key": AWS_ACCESS_KEY_ID,
            "secret_key": AWS_SECRET_ACCESS_KEY,
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "region_name": AWS_S3_REGION_NAME,
            "custom_domain": AWS_S3_CUSTOM_DOMAIN,
            "default_acl": None,
            "querystring_auth": False,
            "location": "static",
        },
    },
}

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"

# Static files (CSS, JavaScript, Images)
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"

# Media files (uploads)
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"

# Additional settings
AWS_S3_FILE_OVERWRITE = True
AWS_S3_VERIFY = True

# Sentry
SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN and not DEBUG:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
            CeleryIntegration(),
        ],
        traces_sample_rate=1.0,
        send_default_pii=True,
    )
