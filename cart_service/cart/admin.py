# order/admin.py

from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_id", "created_at")
    list_filter = ("customer_id",)
    search_fields = ("id", "customer_id")
    ordering = ("-created_at",)


@admin.register(CartItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product_id",
        "product_name",
        "product_type",
        "quantity",
        "image_urls",
        "price",
    )
    search_fields = ("product_name", "product_type")
