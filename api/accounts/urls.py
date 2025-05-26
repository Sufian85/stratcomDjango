from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from . views import *

urlpatterns = [
    path("register", register, name="register"),
    path("login", login, name="login"),
    path("logout", logout_view, name="logout"),
    path("logout-all", logout_all_view, name="logout_all"),
    path("change-password", change_password, name="change_password"),
    path("activate/<str:uidb64>/<str:token>", activate_account, name="activate_account"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path('api/token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path("profile", user_profile, name="profile"),
    path("request-password-reset", request_password_reset, name="request_password_reset"),
    path('reset-password/<str:uidb64>/<str:token>', reset_password, name='reset-password')
]