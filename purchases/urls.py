from typing import List

from django.urls import path

from .views import CreateCategory, DeleteCategory, DeleteProduct, home, current_product, EditProduct, CreateProduct

urlpatterns: List = [
    path("", home, name="home"),
    path("<slug:category_slug>", home, name="home"),
    path("product/<slug:slug>", current_product, name="product"),
    
    path("create_product/", CreateProduct.as_view(), name="create_product"),
    path("create_category/", CreateCategory.as_view(), name="create_category"),
    
    path("edit_product/<slug:slug>", EditProduct.as_view(), name="edit_product"),
    
    path("delete_product/<slug:slug>", DeleteProduct.as_view(), name="delete_product"),
    path("delete_category/<slug:slug>", DeleteCategory.as_view(), name="delete_category"),
]
