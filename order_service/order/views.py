from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
import requests
from .models import Order, OrderItem, OrderStatus
from .serializers import OrderSerializer

CUSTOMER_API = "http://127.0.0.1:8005/api/customers/"
PRODUCT_APIS = {
    "books": "http://127.0.0.1:8002/api/books/",
    "phones": "http://127.0.0.1:8008/api/phones/",
    "clothes": "http://127.0.0.1:8004/api/clothes/",
}
CART_API = "http://127.0.0.1:8003/"


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        customer_id = request.data.get("customer_id")
        items = request.data.get("items", [])

        # Validate Customer
        customer_resp = requests.get(f"{CUSTOMER_API}{customer_id}/")
        print(f"customer_resp={customer_resp}")
        if customer_resp.status_code != 200:
            return Response(
                {"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Fetch Product Data
        total_price = 0
        order_items = []
        for item in items:
            category = item.get("category")
            product_id = item.get("product_id")
            quantity = item.get("quantity", 1)

            if category not in PRODUCT_APIS:
                return Response(
                    {"error": f"Invalid category: {category}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            product_resp = requests.get(f"{PRODUCT_APIS[category]}{product_id}/")
            if product_resp.status_code != 200:
                return Response(
                    {"error": f"Product {product_id} not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            product_data = product_resp.json()
            total_price += float(product_data["price"]) * quantity
            delete_in_cart = requests.delete(
                f"{CART_API}{customer_id}/remove/{category}/{product_id}/"
            )
            print("delete_in_cart", delete_in_cart.json())
            order_items.append(
                {
                    "category": category,
                    "product_id": product_id,
                    "product_name": product_data["name"],
                    "product_image": product_data["url"],
                    "price": product_data["price"],
                    "quantity": quantity,
                }
            )

        # Save Order
        order = Order.objects.create(customer_id=customer_id, total_price=total_price)
        for item in order_items:
            OrderItem.objects.create(order=order, **item)

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def update_status(self, request, pk=None):
        order = self.get_object()
        status = request.data.get("status")
        if status not in OrderStatus.values:
            return Response(
                {"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST
            )
        order.status = status
        order.save()
        return Response(OrderSerializer(order).data)

    @action(
        detail=False, methods=["get"], url_path="by-customer/(?P<customer_id>[^/.]+)"
    )
    def get_by_customer(self, request, customer_id=None):
        orders = Order.objects.filter(customer_id=customer_id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
