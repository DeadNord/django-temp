import jwt
from datetime import timedelta, datetime
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from uuid import uuid4

# Получаем секреты и настройки времени жизни токенов из settings.py
JWT_SECRET_KEY = settings.JWT_SECRET_KEY
ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN  # В секундах
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN  # В секундах

# Сообщения об ошибках
TOKEN_ERRORS = {
    "JWT_SECRET_MISSING": "JWT секрет не задан.",
    "TOKEN_EXPIRED": "Токен истек.",
    "INVALID_TOKEN": "Неверный токен.",
    "AUTHENTICATION_FAILED": "Аутентификация не удалась.",
}


# Преобразование времени истечения в секунды
def convert_expires_in_to_seconds(expires_in: str) -> int:
    if expires_in.endswith("m"):
        return int(expires_in[:-1]) * 60
    elif expires_in.endswith("h"):
        return int(expires_in[:-1]) * 3600
    raise ValueError("Invalid format for expiration time")


# Генерация Access Token
def generate_access_token(user_id: str) -> str:
    expires_in_seconds = convert_expires_in_to_seconds(ACCESS_TOKEN_EXPIRES_IN)
    return generate_token(user_id, expires_in_seconds)


# Генерация Refresh Token
def generate_refresh_token() -> str:
    expires_in_seconds = convert_expires_in_to_seconds(REFRESH_TOKEN_EXPIRES_IN)
    return generate_token(str(uuid4()), expires_in_seconds)


# Общая функция генерации JWT токена
def generate_token(id: str, expires_in: int) -> str:
    if not JWT_SECRET_KEY:
        raise Exception(TOKEN_ERRORS["JWT_SECRET_MISSING"])

    expiration_time = datetime.utcnow() + timedelta(seconds=expires_in)
    payload = {"id": id, "exp": expiration_time}

    try:
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
        return token
    except Exception as e:
        raise Exception(f"Ошибка при генерации токена: {str(e)}")


# Проверка и декодирование JWT токена
def verify_token(token: str) -> str:
    if not JWT_SECRET_KEY:
        raise Exception(TOKEN_ERRORS["JWT_SECRET_MISSING"])

    try:
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        return decoded_token["id"]  # Возвращаем ID пользователя из токена
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed(TOKEN_ERRORS["TOKEN_EXPIRED"])
    except jwt.InvalidTokenError:
        raise AuthenticationFailed(TOKEN_ERRORS["INVALID_TOKEN"])
