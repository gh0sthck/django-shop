from django.contrib import admin

from .models import Product, Category, Comments


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "price", "available", "create", "updated", "image"]
    list_filter = ["available", "create", "updated"]
    list_editable = ["price", "available"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ["product", "text", "client", "rating", "created", "updated"]
    list_filter = ["rating", "created", "updated"]
