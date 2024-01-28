from django import forms

from .models import Category

categories_to_choice = {category.name: category.name for category in Category.objects.all()}


class CategoryForm(forms.Form):
    select_category = forms.ChoiceField(
        required=False,
        choices=categories_to_choice,
        label="Выберите категорию"
    )
