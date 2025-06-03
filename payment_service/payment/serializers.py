from rest_framework import serializers
from .models import Payment
import requests

ORDER_API = "http://127.0.0.1:8006/order/orders/"


class PaymentSerializer(serializers.ModelSerializer):
    order_details = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = "__all__"

    def get_order_details(self, obj):
        try:
            response = requests.get(f"{ORDER_API}{obj.order_id}/")
            if response.status_code == 200:
                return response.json()
            return {"error": "Order not found"}
        except requests.exceptions.RequestException:
            return {"error": "Order service unavailable"}
