from typing import Optional

from django.shortcuts import render, redirect
from django.db.models import QuerySet
from django.http import HttpResponse

from .forms import CategoryForm, CreateProductForm
from .models import Product, Category


def home(request, category_slug=None) -> HttpResponse:
    categories: Optional[QuerySet[Category]] = Category.objects.all()
    category = None
    product_list: QuerySet[Product] = Product.available_products.all()
    form = CategoryForm()

    if category_slug or "select_category" in request.GET:
        if "select_category" in request.GET:
            category = Category.objects.get(name=request.GET["select_category"])
        elif category_slug:
            category = Category.objects.get(slug=category_slug)
        product_list = Product.available_products.filter(category=category)
        categories = None

    return render(request, "home.html", {"products": product_list, "categories": categories,
                                         "form": form, "category": category})


def current_product(request, slug) -> HttpResponse:
    product: Product = Product.available_products.get(slug=slug)

    return render(request, "current_product.html", {"product": product})


def create_product(request) -> HttpResponse:
    if request.method == "POST":
        form = CreateProductForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.POST)
            print(request.FILES)
            form.save()
            return redirect("home")
    else:
        form = CreateProductForm()

    return render(request, "create_product.html", {"form": form})


def edit_product(request, slug) -> HttpResponse:
    product: Product = Product.objects.get(slug=slug)
    if request.method == "POST":
        form = CreateProductForm(request.POST, request.FILES, instance=product)
        if form.has_changed():
            form.save()
            return redirect("home")
    else:
        form = CreateProductForm(instance=product)

    return render(request, "create_product.html", {"form": form})
