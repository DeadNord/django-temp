import os
from pathlib import Path
from pymongo import MongoClient
from environs import Env

env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Auth Settings
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
COOKIE_SECRET_KEY = os.environ.get("COOKIE_SECRET_KEY")
ACCESS_TOKEN_EXPIRES_IN = os.environ.get("ACCESS_TOKEN_EXPIRES_IN", 60 * 60 * 24 * 7)
REFRESH_TOKEN_EXPIRES_IN = os.environ.get("REFRESH_TOKEN_EXPIRES_IN", 60 * 60 * 24 * 30)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
PYTHON_ENV = os.environ.get("PYTHON_ENV", "development")
DEBUG = PYTHON_ENV == "development"


ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

if PYTHON_ENV == "development":
    CORS_ALLOW_ALL_ORIGINS = True
else:
    raw_cors_origins = os.environ.get("CORS_ALLOWED_ORIGINS", "")
    CORS_ALLOWED_ORIGINS = raw_cors_origins.split(",") if raw_cors_origins else []

CORS_ALLOW_HEADERS = [
    "Accept",
    "Accept-encoding",
    "Authorization",
    "Content-type",
    "Origin",
    "User-agent",
    "C-csrftoken",
    "C-requested-with",
    "Cookie",
    "Referer",
]

CORS_ALLOW_CREDENTIALS = True


# Application definition
GLOBAL_RATE_LIMIT = os.environ.get("RATE_LIMITING", "100/hour")

REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": ["rest_framework.throttling.ScopedRateThrottle"],
    "DEFAULT_THROTTLE_RATES": {"global": GLOBAL_RATE_LIMIT},
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "api",
    "rest_framework",
    "drf_spectacular",
]


SPECTACULAR_SETTINGS = {
    "TITLE": "Users Service API",
    "DESCRIPTION": "This service allows users to manage their financial transactions and budgets, categorize transactions, and view financial analytics.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "LICENSE": {
        "name": "MIT License",
    },
    "SERVERS": [
        {"url": os.environ.get("SERVICE_URL", "http://localhost:8000")},
    ],
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
    },
    "COMPONENT_SPLIT_REQUEST": True,
    "SECURITY": [
        {"Bearer": []},
    ],
    "SECURITY_SCHEMES": {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": 'Введите ваш JWT токен в формате "Bearer {token}"',
        },
    },
    "USE_SESSION_AUTH": False,
    "EXTENSIONS_INFO": [
        "api.middlewares.authentication_extensions.JWTAuthenticationScheme",
    ],
}


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# Получаем параметры подключения к MongoDB из переменных окружения
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://<username>:<password>@cluster0.mongodb.net/<database_name>?retryWrites=true&w=majority",
)
MONGO_DB_NAME = os.getenv("MONGO_DATABASE", "your_mongo_database")
MONGO_USER = os.getenv("MONGO_USER", "<username>")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "<password>")


# Подключаемся к MongoDB через PyMongo
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# APPEND_SLASH = False
SECURE_SSL_REDIRECT = False
