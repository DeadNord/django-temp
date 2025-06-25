"""
Django settings template for a **zero‑project core** that runs **Django + PostgreSQL** only.
Copy it into `config/settings.py` (or split into `base.py`/`dev.py`/`prod.py` if you prefer).
All values are pulled from environment variables with sensible defaults so the project
can boot locally with almost zero configuration, while remaining 12‑factor compliant
in staging/production.
"""

from __future__ import annotations

import os
from pathlib import Path

from environs import Env
import dj_database_url

# ---------------------------------------------------------------------------
# Environment & paths
# ---------------------------------------------------------------------------
env = Env()
env.read_env()

BASE_DIR: Path = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Core settings
# ---------------------------------------------------------------------------
PYTHON_ENV: str = env.str("PYTHON_ENV", "development")
DEBUG: bool = PYTHON_ENV == "development"

SECRET_KEY: str = env.str("DJANGO_SECRET_KEY", "⚠️  change‑me‑in‑production ⚠️")

ALLOWED_HOSTS: list[str] = env.list(
    "DJANGO_ALLOWED_HOSTS", default=["localhost", "127.0.0.1"]
)

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOWED_ORIGINS: list[str] = env.list("CORS_ALLOWED_ORIGINS", default=[])

CORS_ALLOW_HEADERS: list[str] = [
    "Accept",
    "Accept-encoding",
    "Authorization",
    "Content-type",
    "Origin",
    "User-agent",
    "C-csrftoken",
    "__csrftoken",
    "C-requested-with",
    "Cookie",
    "Referer",
]
CORS_ALLOW_CREDENTIALS: bool = True

# ---------------------------------------------------------------------------
# Rate limiting & DRF
# ---------------------------------------------------------------------------
GLOBAL_RATE_LIMIT = env.str("RATE_LIMITING", "100/hour")

REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.ScopedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "global": GLOBAL_RATE_LIMIT,
    },
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": [
        # "rest_framework.permissions.IsAuthenticated",
        "rest_framework.permissions.AllowAny"
        ],
}

# ---------------------------------------------------------------------------
# Apps
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",  # <- enable PostgreSQL specific fields
    # Third‑party
    "corsheaders",
    "rest_framework",
    "drf_spectacular",
    # Local
    "api",
]

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# ---------------------------------------------------------------------------
# Database (PostgreSQL only)
# ---------------------------------------------------------------------------
# Priority 1: full DATABASE_URL (e.g. render.com, Heroku, Fly.io)
DATABASE_URL: str = env.str(
    "DATABASE_URL",
    default="postgres://{user}:{password}@{host}:{port}/{name}".format(
        user=env.str("POSTGRES_USER", "postgres"),
        password=env.str("POSTGRES_PASSWORD", "postgres"),
        host=env.str("POSTGRES_HOST", "localhost"),
        port=env.str("POSTGRES_PORT", "5432"),
        name=env.str("POSTGRES_DB", "app_db"),
    ),
)

DATABASES = {
    "default": dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        ssl_require=not DEBUG,
    )
}

# ---------------------------------------------------------------------------
# Password validation
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Internationalisation
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = env.str("TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static files
# ---------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ---------------------------------------------------------------------------
# Misc
# ---------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SECURE_SSL_REDIRECT = not DEBUG

# ---------------------------------------------------------------------------
# OpenAPI / drf-spectacular
# ---------------------------------------------------------------------------
SPECTACULAR_SETTINGS = {
    "TITLE": "Zero‑Project Core API",
    "DESCRIPTION": (
        "Boilerplate project powered by Django REST Framework and PostgreSQL "
        "with JWT auth out of the box."
    ),
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "LICENSE": {"name": "MIT License"},
    "SERVERS": [
        {"url": ""},
    ],
    "SWAGGER_UI_SETTINGS": {"deepLinking": True},
    "COMPONENT_SPLIT_REQUEST": True,
    # "SECURITY": [{"Bearer": []}],
    # "SECURITY_SCHEMES": {
    #     "Bearer": {
    #         "type": "http",
    #         "scheme": "bearer",
    #         "bearerFormat": "JWT",
    #         "description": 'Введите JWT в формате "Bearer <token>"',
    #     }
    # },
    "USE_SESSION_AUTH": False,
    # "EXTENSIONS_INFO": [
    #     "api.middlewares.authentication_extensions.JWTAuthenticationScheme",
    # ],
}
