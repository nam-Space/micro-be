# order/admin.py

from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        "product_name",
        "product_image",
        "category",
        "product_id",
        "price",
        "quantity",
    )
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_id", "total_price", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("id", "customer_id")
    ordering = ("-created_at",)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product_name", "category", "price", "quantity")
    search_fields = ("product_name", "category")
    readonly_fields = (
        "order",
        "product_name",
        "product_image",
        "category",
        "product_id",
        "price",
        "quantity",
    )
