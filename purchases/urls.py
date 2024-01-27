from typing import List

from django.urls import path

from .views import home, product_list, category_list

urlpatterns: List = [
    path("", home, name="home"),
    path("products/", product_list, name="product_list"),
    path("categories/", category_list, name="category_list"),
]
