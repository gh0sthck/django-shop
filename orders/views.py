from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from cart.cart import Cart
from orders.forms import CreateOrderForm
from orders.models import OrderItem


def create_order(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        cart = Cart(request)
        if request.method == "POST":
            form = CreateOrderForm(request.POST)
            if form.is_valid():
                order = form.save()
                for item in cart:
                    OrderItem.objects.create(order=order,
                                             product=item["product"],
                                             price=item["price"],
                                             count=item["count"])
                    cart.clear()

                    return render(request, "order_created.html", {"order": order})
        else:
            form = CreateOrderForm()

        return render(request, "order_create.html", {"cart": cart, "form": form})
    else:
        return redirect("user_login")