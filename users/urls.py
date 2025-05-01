from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import UserLoginView, UserRegisterView, UserRecoverPasswordView

app_name = "users"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("recover-password/", UserRecoverPasswordView.as_view(), name="recover-password"),
    path("logout/", LogoutView.as_view(), name="logout")
]