from typing import List

from django.urls import path

from .views import home, current_product, current_category

urlpatterns: List = [
    path("", home, name="home"),
    path("product/<slug:slug>", current_product, name="product"),
    path("category/<slug:slug>", current_category, name="category")
]
