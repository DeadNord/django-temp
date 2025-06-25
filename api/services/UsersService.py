from api.models import User
from config.settings import db
from bson.objectid import ObjectId  # Для работы с ObjectId в MongoDB
from django.core.exceptions import ValidationError
from ..helpers.jwt_helper import (
    generate_access_token,
    generate_refresh_token,
    verify_token,
)
import bcrypt


class UsersService:

    def sign_in_service(self, sign_in_data):
        email = sign_in_data["email"]
        password = sign_in_data["password"]

        # Найти пользователя по email
        users_collection = db["users"]  # Используем PyMongo для доступа к коллекции
        user = users_collection.find_one({"email": email})
        if not user:
            raise ValidationError("User not found")

        # Проверить пароль
        if not bcrypt.checkpw(
            password.encode("utf-8"), user["password"].encode("utf-8")
        ):
            raise ValidationError("Invalid password")

        access_token = generate_access_token(str(user["_id"]))
        refresh_token = generate_refresh_token()

        # Обновить токены пользователя
        users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"access_token": access_token, "refresh_token": refresh_token}},
        )

        return {"accessToken": access_token, "refreshToken": refresh_token}

    def sign_up_service(self, sign_up_data):
        email = sign_up_data["email"]
        users_collection = db["users"]

        if users_collection.find_one({"email": email}):
            raise ValidationError("User with this email already exists")

        hashed_password = bcrypt.hashpw(
            sign_up_data["password"].encode("utf-8"), bcrypt.gensalt()
        )

        # Создаем экземпляр класса User, чтобы использовались значения по умолчанию
        new_user = User(
            name=sign_up_data["name"],
            email=email,
            password=hashed_password.decode("utf-8"),
        )

        # Сохраняем пользователя в базу данных
        new_user.save()

    def sign_out_service(self, refresh_token):
        users_collection = db["users"]

        user = users_collection.find_one({"refresh_token": refresh_token})
        if not user:
            raise ValidationError("User not found")

        # Удаляем токены
        users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"access_token": None, "refresh_token": None}},
        )

    def refresh_access_service(self, refresh_token):
        # Верификация refresh токена
        user_id = verify_token(refresh_token, is_refresh=True)
        users_collection = db["users"]

        user = users_collection.find_one({"refresh_token": refresh_token})
        if not user:
            raise ValidationError("Invalid refresh token")

        new_access_token = generate_access_token(str(user["_id"]))

        # Обновляем access_token в MongoDB
        users_collection.update_one(
            {"_id": user["_id"]}, {"$set": {"access_token": new_access_token}}
        )

        return {"accessToken": new_access_token}

    def get_user_info(self, user_id):
        users_collection = db["users"]

        # Находим пользователя по ObjectId
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise ValidationError("User not found")

        return {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "companies": user.get("companies", []),
        }
