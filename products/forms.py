from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("full_name", "address", "phone", "email")
        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Иванов Иван Иванович"
            }),
            "address": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "ул. Пушкина, д. 1, кв. 1"

            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "+7XXXXXXXXXX или 8XXXXXXXXXX"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "example@email.com"
            }),
        }
