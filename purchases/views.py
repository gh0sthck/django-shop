from django.shortcuts import render
from django.db.models import QuerySet
from django.http import HttpResponse

from .models import Product, Category


def home(request, category_slug=None) -> HttpResponse:
    category: Category | QuerySet[Category] = Category.objects.all()
    product_list: QuerySet[Product] = Product.available_products.all()

    if category_slug:
        category = Category.objects.filter(slug=category_slug)
        product_list = Product.available_products.filter(category=category[0])

    return render(request, "home.html", {"products": product_list, "category": category})


def current_product(request, slug) -> HttpResponse:
    product: Product = Product.available_products.get(slug=slug)

    return render(request, "current_product.html", {"product": product})