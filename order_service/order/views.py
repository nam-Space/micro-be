import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Order, OrderItem
from .serializers import OrderSerializer

CUSTOMER_API = "http://127.0.0.1:6789/api/customers/"
CART_API = "http://127.0.0.1:8080/"
PRODUCT_APIS = {
    "books": "http://127.0.0.1:9876/api/books/",
    "phones": "http://127.0.0.1:9876/api/phones/",
    "clothes": "http://127.0.0.1:9876/api/clothes/",
}

class CreateOrderView(APIView):
    @swagger_auto_schema(
        operation_description="Create a new order for a customer.",
        responses={201: OrderSerializer()},
        manual_parameters=[
            openapi.Parameter(
                "customer_id",
                openapi.IN_PATH,
                description="ID of the customer placing the order",
                type=openapi.TYPE_INTEGER,
            )
        ],
    )
    def post(self, request, customer_id):
        # Validate customer
        customer_response = requests.get(f"{CUSTOMER_API}{customer_id}/")
        if customer_response.status_code != 200:
            return Response({"error": "Invalid customer"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch cart items
        cart_response = requests.get(f"{CART_API}{customer_id}/")
        if cart_response.status_code != 200:
            return Response({"error": "Failed to fetch cart"}, status=status.HTTP_400_BAD_REQUEST)
        cart_items = cart_response.json()

        total_price = 0
        order_items = []

        # Validate product availability
        for item in cart_items:
            product_type, product_id, quantity = item["product_type"], item["product_id"], item["quantity"]
            product_url = f"{PRODUCT_APIS[product_type]}{product_id}/"
            product_response = requests.get(product_url)

            if product_response.status_code != 200:
                return Response(
                    {"error": f"Product {product_type} {product_id} not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            product_data = product_response.json()
            total_price += product_data["price"] * quantity
            order_items.append(
                {
                    "product_type": product_type,
                    "product_id": product_id,
                    "quantity": quantity,
                    "price": product_data["price"],
                }
            )

        # Save order
        order = Order.objects.create(customer_id=customer_id, total_price=total_price)
        for item in order_items:
            OrderItem.objects.create(order=order, **item)

        # Clear cart
        requests.delete(f"{CART_API}{customer_id}/clear/")

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
