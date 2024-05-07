from django import forms

from .models import ShopClient


class RegisterClientForm(forms.ModelForm):
    gender = forms.ChoiceField(choices={"f": "Женский", "m": "Мужской"}, label="Пол")
    password = forms.CharField(min_length=8, label="Пароль", widget=forms.PasswordInput)
    password_repeat = forms.CharField(min_length=8, label="Повтор пароля", widget=forms.PasswordInput)

    class Meta:
        model = ShopClient
        fields = ["username", "email", "avatar", "gender", "password"]

    def clean_password_repeat(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password_repeat"]:
            raise forms.ValidationError("Пароли не совпадают")
        else:
            return cd["password_repeat"]
