from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import phone_regex


class CustomUser(AbstractUser):
    choices = (
        ("m", "male"),
        ("f", "female")
    )
    phone = models.CharField(validators=[phone_regex], max_length=255, verbose_name="Номер телефона")
    avatar = models.ImageField(upload_to="users_avatar/", blank=True, null=True, verbose_name="Аватар")
    birth_date = models.DateField(blank=True, null=True, verbose_name="День рождения")
    gender = models.CharField(choices=choices, blank=True, null=True, verbose_name="Гендер")
    address_default = models.TextField(blank=True, null=True, verbose_name="Адрес")
    email_confirm = models.BooleanField(default=False, verbose_name="Подтверждение почты")
    phone_confirm = models.BooleanField(default=False, verbose_name="Подтверждение телефона")
    newsletter_subscribed = models.BooleanField(default=False, blank=True, null=True,
                                                verbose_name="Согласие на рассылку")
    last_activity = models.DateTimeField(auto_now_add=True, verbose_name="Последняя активность")
    is_banned = models.BooleanField(default=False, verbose_name="Заблокирован ли пользователь")
    notes_admin = models.TextField(blank=True, null=True, verbose_name="Внутренние заметки админа")
