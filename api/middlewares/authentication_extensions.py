from drf_spectacular.extensions import OpenApiAuthenticationExtension


class JWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "api.middlewares.authentication.JWTAuthentication"
    name = "Bearer"

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": 'Введите ваш JWT токен в формате "Bearer {token}"',
        }
