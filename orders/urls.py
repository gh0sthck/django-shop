from typing import List

from django.urls import path

from .views import create_order

urlpatterns: List = [
    path("create/", create_order, name="order_create"),
]