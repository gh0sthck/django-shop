from typing import List

from django.urls import path

from .views import home, current_product, create_product

urlpatterns: List = [
    path("", home, name="home"),
    path("<slug:category_slug>", home, name="home"),
    path("product/<slug:slug>", current_product, name="product"),
    path("create_product/", create_product, name="create_product"),
]
