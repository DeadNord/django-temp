from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from .middlewares.authentication import JWTAuthentication
from .services.UsersService import UsersService
from .helpers.cookies_helper import save_token_cookies, clear_token_cookies


# BaseView for common properties like rate limiting
class BaseView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "global"


# SignIn view
class SignInView(BaseView):

    @extend_schema(
        request=inline_serializer(
            name="SignInRequest",
            fields={
                "email": serializers.EmailField(help_text="User's email address"),
                "password": serializers.CharField(
                    help_text="Password for authentication",
                    style={"input_type": "password"},
                ),
            },
        ),
        responses={
            200: inline_serializer(
                name="SignInResponse",
                fields={
                    "accessToken": serializers.CharField(help_text="Access token"),
                },
            ),
            400: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "SignIn Request Example",
                value={"email": "user@example.com", "password": "SecurePassword123!"},
                request_only=True,
            ),
            OpenApiExample(
                "SignIn Response Example",
                value={"accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."},
                response_only=True,
            ),
        ],
        description="Authenticate user and return access token.",
        summary="User Sign In",
        tags=["Authentication"],
    )
    def post(self, request):
        user_service = UsersService()
        sign_in_data = request.data
        try:
            tokens = user_service.sign_in_service(sign_in_data)
            response = Response(
                {"accessToken": tokens["accessToken"]}, status=status.HTTP_200_OK
            )
            save_token_cookies(response, "refreshToken", tokens["refreshToken"], 1440)
            return response
        except ValidationError as e:
            return Response(
                {"error": str(e.detail)}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# SignUp view
class SignUpView(BaseView):

    @extend_schema(
        request=inline_serializer(
            name="SignUpRequest",
            fields={
                "email": serializers.EmailField(help_text="User's email address"),
                "name": serializers.CharField(help_text="Full name of the user"),
                "password": serializers.CharField(
                    help_text="Password for authentication",
                    style={"input_type": "password"},
                    min_length=8,
                ),
            },
        ),
        responses={
            201: inline_serializer(
                name="SignUpResponse",
                fields={
                    "message": serializers.CharField(
                        help_text="Registration confirmation message"
                    ),
                },
            ),
            400: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "SignUp Request Example",
                value={
                    "email": "user@example.com",
                    "name": "John Doe",
                    "password": "SecurePassword123!",
                },
                request_only=True,
            ),
            OpenApiExample(
                "SignUp Response Example",
                value={"message": "User registered successfully"},
                response_only=True,
            ),
        ],
        description="Register a new user.",
        summary="User Sign Up",
        tags=["Authentication"],
    )
    def post(self, request):
        user_service = UsersService()
        sign_up_data = request.data
        try:
            user_service.sign_up_service(sign_up_data)
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            return Response(
                {"error": str(e.detail)}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# SignOut view
class SignOutView(BaseView):

    @extend_schema(
        responses={
            204: inline_serializer(
                name="SignOutResponse",
                fields={
                    "message": serializers.CharField(
                        help_text="Sign out confirmation message"
                    ),
                },
            ),
            400: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT,
        },
        description="Sign out the user.",
        summary="User Sign Out",
        tags=["Authentication"],
    )
    def post(self, request):
        user_service = UsersService()
        refresh_token = request.COOKIES.get("refreshToken")
        try:
            user_service.sign_out_service(refresh_token)
            response = Response(status=status.HTTP_204_NO_CONTENT)
            clear_token_cookies(response, "refreshToken")
            return response
        except ValidationError as e:
            return Response(
                {"error": str(e.detail)}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# Refresh Token view
class RefreshTokenView(BaseView):

    @extend_schema(
        responses={
            200: inline_serializer(
                name="RefreshTokenResponse",
                fields={
                    "accessToken": serializers.CharField(help_text="New access token"),
                },
            ),
            400: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT,
        },
        description="Refresh the access token using the refresh token.",
        summary="Refresh Access Token",
        tags=["Authentication"],
    )
    def get(self, request):
        user_service = UsersService()
        refresh_token = request.COOKIES.get("refreshToken")
        try:
            new_tokens = user_service.refresh_access_service(refresh_token)
            return Response(
                {"accessToken": new_tokens["accessToken"]}, status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response(
                {"error": str(e.detail)}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# UserInfo view
class UserInfoView(BaseView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: inline_serializer(
                name="UserInfoResponse",
                fields={
                    "id": serializers.CharField(
                        help_text="User's unique ID",
                    ),
                    "name": serializers.CharField(help_text="Full name of the user"),
                    "email": serializers.EmailField(help_text="User's email address"),
                    "companies": serializers.ListField(
                        child=inline_serializer(
                            name="CompanyInfo",
                            fields={
                                "companyId": serializers.CharField(
                                    help_text="Company ID"
                                ),
                                "employeeId": serializers.CharField(
                                    help_text="Employee ID"
                                ),
                                "roles": serializers.ListField(
                                    child=serializers.CharField(
                                        help_text="Role in the company"
                                    ),
                                    help_text="List of roles in the company",
                                ),
                                "projectRolesId": serializers.ListField(
                                    child=serializers.CharField(
                                        help_text="Project Role ID"
                                    ),
                                    help_text="List of project roles IDs",
                                ),
                            },
                        ),
                        help_text="List of companies associated with the user",
                    ),
                },
            ),
            401: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT,
        },
        description="Retrieve information about the authenticated user.",
        summary="Get User Info",
        tags=["User"],
    )
    def get(self, request):
        user_service = UsersService()
        user_id = request.user["_id"]
        try:
            user_info = user_service.get_user_info(user_id)
            return Response(user_info, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
