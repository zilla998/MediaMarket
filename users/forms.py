from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .validators import phone_regex


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'phone','password1', 'password2', 'birth_date']


class UserRecoverPasswordForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-input'}))
    class Meta:
        model = get_user_model()
        fields = ['email']