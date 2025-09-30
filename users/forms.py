from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Логин", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    password = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-input"})
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "password"]


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Логин", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    password1 = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-input"})
    )
    password2 = forms.CharField(
        label="Повтор пароля", widget=forms.PasswordInput(attrs={"class": "form-input"})
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "phone", "password1", "password2", "birth_date"]


class UserRecoverPasswordForm(forms.Form):
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-input"})
    )

    class Meta:
        model = get_user_model()
        fields = ["email"]


class UserProfileSettingsForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Имя", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    last_name = forms.CharField(
        label="Фамилия", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-input"})
    )
    phone = forms.CharField(
        label="Телефон", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    password = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-input"})
    )
    password2 = forms.CharField(
        label="Повтор пароля", widget=forms.PasswordInput(attrs={"class": "form-input"})
    )
    avatar = forms.ImageField(
        label="Аватар", widget=forms.FileInput(attrs={"class": "form-input"})
    )
    birth_date = forms.DateField(
        label="Дата рождения", widget=forms.DateInput(attrs={"class": "form-input"})
    )
    gender = forms.BooleanField(
        label="Пол", widget=forms.CheckboxInput(attrs={"class": "form-input"})
    )

    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "password",
            "password2",
            "avatar",
            "birth_date",
            "gender",
        ]
