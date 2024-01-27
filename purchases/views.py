from django.shortcuts import render
from django.db.models import QuerySet
from django.http import HttpResponse

from .models import Product, Category


def home(request) -> HttpResponse:
    prods: QuerySet[Product] = Product.available_products.all()

    return render(request, "home.html", {"prod": prods})


def current_product(request, slug) -> HttpResponse:
    product: Product = Product.available_products.get(slug=slug)

    return render(request, "current_product.html", {"product": product})


def current_category(request, slug) -> HttpResponse:
    category: Category = Category.objects.get(slug=slug)

    return render(request, "current_category.html", {"category": category})