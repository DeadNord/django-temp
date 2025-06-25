from django.urls import path
from .views import SignInView, SignUpView, SignOutView, RefreshTokenView, UserInfoView

urlpatterns = [
    path("signIn/", SignInView.as_view(), name="sign_in"),
    path("signUp/", SignUpView.as_view(), name="sign_up"),
    path("signOut/", SignOutView.as_view(), name="sign_out"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh_token"),
    path("user/", UserInfoView.as_view(), name="user_info"),
]
