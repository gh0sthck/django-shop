from django.contrib import admin

from users.models import ShopClient


@admin.register(ShopClient)
class ShopClientAdmin(admin.ModelAdmin):
    list_display = ["user", "avatar", "gender"]
    raw_id_fields = ["user"]