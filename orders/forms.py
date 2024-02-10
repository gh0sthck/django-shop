from django import forms
from django.core.exceptions import ValidationError

from .models import Order


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["first_name", "last_name", "phone", "email", "address",
                  "postal_code", "city"]

    def clean_phone(self):
        cd = self.cleaned_data

        if (not str(cd["phone"]).startswith("7")) and (not str(cd["phone"]).startswith("8")):
            raise ValidationError("Неверно набран номер телефона (номер телефона должен начинаться с 7 или 8")
        else:
            return cd["phone"]