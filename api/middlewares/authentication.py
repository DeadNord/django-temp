# myapp/authentication.py

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from bson.objectid import ObjectId
import os
from wms_utils.db.db import MongoConnection

mongo_connection = MongoConnection()
db = mongo_connection.get_db()

# Инициализация переменных окружения
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")


class JWTAuthentication(BaseAuthentication):
    """
    Кастомный класс аутентификации для проверки JWT токенов и получения пользователя из MongoDB.
    """

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise AuthenticationFailed("No authentication header provided")

        try:
            print(auth_header)
            token = auth_header.split(" ")[1]  # Извлекаем токен из заголовка
            decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])

            # Ищем пользователя по ID из токена в MongoDB
            users_collection = db["users"]  # Коллекция пользователей
            user = users_collection.find_one(
                {"_id": ObjectId(decoded_token["user_id"])}
            )

            if not user:
                raise AuthenticationFailed("User not found or invalid token")

            # Возвращаем пользователя и токен
            return (user, token)
        except IndexError:
            raise AuthenticationFailed("Token not provided")
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Access token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

    def authenticate_header(self, request):
        return "Bearer"
