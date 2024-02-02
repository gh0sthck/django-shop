from typing import List

from django.urls import path

from cart.views import cart_detail, add_cart, cart_remove

urlpatterns: List = [
    path("", cart_detail, name="cart_detail"),
    path("add/<int:product_id>", add_cart, name="add_cart"),
    path("remove/<int:product_id>", cart_remove, name="remove_cart"),
]