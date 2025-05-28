from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    # phone = forms.CharField(max_length=255, label="Номер телефона")
    class Meta:
        model = Order
        fields = ('full_name', "address", "phone", "email")
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
        }


