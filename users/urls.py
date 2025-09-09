from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import (
    UserLoginView,
    UserRegisterView,
    UserRecoverPasswordView,
    user_profile,
    UserProfileSettingsView,
    user_profile_orders,
)

app_name = "users"

urlpatterns = [
    path("profile/<pk>", user_profile, name="user_profile"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path(
        "recover-password/",
        UserRecoverPasswordView.as_view(),
        name="recover-password"
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("settings/",
         UserProfileSettingsView.as_view(),
         name="user_profile_settings"),
    path("orders/<pk>", user_profile_orders, name="user_profile_orders"),
]
