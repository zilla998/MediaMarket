from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from products.models import Order
from users.forms import (
    UserLoginForm,
    UserRegisterForm,
    UserRecoverPasswordForm,
    UserProfileSettingsForm,
)
from users.models import CustomUser


@login_required
def user_profile(request, pk):
    user = CustomUser.objects.get(pk=pk)
    return render(request, "users/profile.html", {"user": user})


@login_required
def user_profile_orders(request, pk):
    user = CustomUser.objects.get(pk=pk)
    orders = Order.objects.filter(user=user).order_by("-created_at")
    return render(
        request, "users/profile_orders.html", {"orders": orders, "user": user}
    )


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "users/login.html"
    extra_context = {"title": "Авторизация"}


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "users/register.html"
    extra_context = {"title": "Регистрация"}
    success_url = reverse_lazy("users:login")


class UserRecoverPasswordView(CreateView):
    form_class = UserRecoverPasswordForm
    template_name = "users/recover_password.html"
    extra_context = {"title": "Восстановление пароля"}


class UserProfileSettingsView(LoginRequiredMixin, CreateView):
    form_class = UserProfileSettingsForm
    template_name = "users/profile_settings.html"
    extra_context = {"title": "Настройки профиля"}
