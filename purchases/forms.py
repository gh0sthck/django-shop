from django import forms

from .models import Category, Product, Comments

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


class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class CommentsForm(forms.ModelForm):
    rating = forms.TypedChoiceField(
        empty_value=0,
        choices={1: "💜", 2: "💜💜", 3: "💜💜💜", 4: "💜💜💜💜", 5: "💜💜💜💜💜"},
        required=False,
        coerce=int,
        label="",
    )
    
    class Meta:
        model = Comments
        fields = ["text", "rating"]
