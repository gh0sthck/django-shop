from typing import Optional

from django.shortcuts import render, get_object_or_404
from django.db.models import QuerySet
from django.http import HttpResponse

from .models import Product, Category


def home(request, category_slug=None) -> HttpResponse:
    category: Optional[Category] = None
    prods: QuerySet[Product] = Product.available_products.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        prods = Product.available_products.filter(category=category)

    return render(request, "home.html", {"products": prods, "category": category})


def current_product(request, slug) -> HttpResponse:
    product: Product = Product.available_products.get(slug=slug)

    return render(request, "current_product.html", {"product": product})


def current_category(request, slug) -> HttpResponse:
    category: Category = Category.objects.get(slug=slug)

    return render(request, "current_category.html", {"category": category})