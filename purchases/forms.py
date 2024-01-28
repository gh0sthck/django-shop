from django import forms

from .models import Category, Product

categories_to_choice = {category.name: category.name for category in Category.objects.all()}


class CategoryForm(forms.Form):
    select_category = forms.ChoiceField(
        required=False,
        choices=categories_to_choice,
        label="Выберите категорию"
    )


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["category", "name", "image", "description", "price", "available"]