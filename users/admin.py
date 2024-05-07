from django.contrib import admin

from .models import ShopClient


@admin.register(ShopClient)
class ShopClientAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "avatar", "gender", "balance"]
