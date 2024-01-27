from typing import List

from django.shortcuts import render
from django.db.models import QuerySet
from django.http import HttpResponse

from .models import Product

def home(request) -> HttpResponse:
    prods: QuerySet[Product] = Product.available_products.all() 

    return render()


def category_list(request, slug) -> HttpResponse:
    ...

def product_list(request, slug) -> HttpResponse:
    ...
