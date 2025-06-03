# payment/admin.py

from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order_id",
        "amount",
        "method",
        "status",
        "customer_id",
        "created_at",
    )
    list_filter = ("status", "method")
    search_fields = ("id", "order_id")
    ordering = ("-created_at",)
