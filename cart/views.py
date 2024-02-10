from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from cart.cart import Cart
from cart.forms import CartAddProductForm
from purchases.models import Product


@require_POST
def add_cart(request: HttpRequest, product_id: int) -> HttpResponse:
    if request.user.is_authenticated:
        cart = Cart(request)
        product = Product.objects.get(id=product_id)
        form = CartAddProductForm(request.POST)

        if form.is_valid():
            clean_data: dict = form.cleaned_data
            cart.add(product=product, count=clean_data["count"],
                     override_count=clean_data["override"])

        return redirect("cart_detail")
    else:
        return redirect("user_login")


@require_POST
def cart_remove(request: HttpRequest, product_id: int) -> HttpResponse:
    if request.user.is_authenticated:
        cart = Cart(request)
        product = Product.objects.get(id=product_id)
        cart.remove(product)
        return redirect("cart_detail")
    else:
        return redirect("user_login")


def cart_detail(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    for item in cart:
        item["update_count_form"] = CartAddProductForm(initial={
            "count": item["count"], "override": True
        })

    return render(request, "cart_detail.html", {"cart": cart})