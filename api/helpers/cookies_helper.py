from django.utils import timezone
from datetime import timedelta
from django.conf import settings

PYTHON_ENV = settings.PYTHON_ENV

DEFAULT_EXPIRES_IN_MINUTES = 60  # Время жизни куки по умолчанию


# Функция для сохранения токена в куки
def save_token_cookies(
    response, key: str, data: str, expires_in_minutes: int = DEFAULT_EXPIRES_IN_MINUTES
):
    expiration_time = timezone.now() + timedelta(minutes=expires_in_minutes)

    # Настройки для secure и sameSite в зависимости от окружения
    secure = PYTHON_ENV != "development"
    same_site = "None" if PYTHON_ENV != "development" else "Lax"

    response.set_cookie(
        key,
        data,
        expires=expiration_time,
        httponly=True,
        secure=secure,
        samesite=same_site,
    )


# Функция для очистки куки
def clear_token_cookies(response, key: str):
    response.delete_cookie(key)
