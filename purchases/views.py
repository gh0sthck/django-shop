from typing import Optional

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import QuerySet
from django.http import HttpResponse, HttpRequest

from cart.cart import Cart
from cart.forms import CartAddProductForm
from .forms import CategoryForm, CreateProductForm
from .models import Product, Category


def home(request: HttpRequest, category_slug=None) -> HttpResponse:
    categories: Optional[QuerySet[Category]] = Category.objects.all()
    category = None
    product_list: QuerySet[Product] = Product.available_products.all()
    form = CategoryForm()
    cart = Cart(request)

    if category_slug or "select_category" in request.GET:
        if "select_category" in request.GET:
            category = Category.objects.get(name=request.GET["select_category"])
        elif category_slug:
            category = Category.objects.get(slug=category_slug)
        product_list = Product.available_products.filter(category=category)
        categories = None

    return render(request, "home.html", {"products": product_list, "categories": categories,
                                         "form": form, "category": category, "cart": cart})


def current_product(request: HttpRequest, slug) -> HttpResponse:
    product: Product = Product.available_products.get(slug=slug)
    cart = Cart(request)
    cart_form = CartAddProductForm()

    return render(request, "current_product.html", {"product": product, "cart_form": cart_form, "cart": cart})


@login_required
def create_product(request: HttpRequest) -> HttpResponse:
    if request.user.has_perms(["purchases.change_product", "purchases.add_product",
                               "purchases.delete_product"]):
        if request.method == "POST":
            form = CreateProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect("home")
        else:
            form = CreateProductForm()

        return render(request, "create_product.html", {"form": form})
    else:
        return HttpResponse("You haven't permissions to that operation")


@login_required
def edit_product(request: HttpRequest, slug) -> HttpResponse:
    if request.user.has_perms(["purchases.change_product", "purchases.add_product",
                               "purchases.delete_product"]):
        product: Product = Product.objects.get(slug=slug)
        if request.method == "POST":
            form = CreateProductForm(request.POST, request.FILES, instance=product)
            if form.has_changed():
                form.save()
                return redirect("home")
        else:
            form = CreateProductForm(instance=product)

        return render(request, "create_product.html", {"form": form})
    else:
        return HttpResponse("You haven't permissions to that operation")
