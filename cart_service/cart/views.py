from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from .utils import check_product_stock, update_product_stock, get_product_by_url
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import json
@api_view(["GET"])
def get_cart(request, customer_id):
    """Retrieve cart details for a customer"""
    cart, created = Cart.objects.get_or_create(customer_id=customer_id)
    serializer = CartSerializer(cart)
    return Response(serializer.data)

# @api_view(["POST"])
# def add_to_cart(request, customer_id, product_id, product_type):
#     """Add an item to the cart"""
#     quantity = request.data.get("quantity", 1)
#     if product_type not in ["books", "phones", "clothes"]:
#         return Response({"error": "Invalid product type"}, status=400)

#     if not check_product_stock(product_type, product_id, quantity):
#         return Response({"error": "Insufficient stock"}, status=400)

#     cart, _ = Cart.objects.get_or_create(customer_id=customer_id)
#     cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id, product_type=product_type)
#     if not created:
#         cart_item.quantity += quantity
#     else:
#         cart_item.quantity = quantity

#     cart_item.save()
#     update_product_stock(product_type, product_id, quantity)

#     return Response({"message": "Item added to cart"})

@api_view(["DELETE"])
def remove_from_cart(request, customer_id, product_id, product_type):
    """Remove an item from the cart"""
    try:
        cart = Cart.objects.get(customer_id=customer_id)
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id, product_type=product_type)
        cart_item.delete()
        return Response({"message": "Item removed from cart"})
    except CartItem.DoesNotExist:
        return Response({"error": "Item not found"}, status=404)

@swagger_auto_schema(
    method="patch",
    request_body=openapi.Schema(
       type=openapi.TYPE_OBJECT,
        required=["quantity", "productId", "customerId", "category"],  # Required fields
        properties={
            "quantity": openapi.Schema(type=openapi.TYPE_INTEGER, description="Quantity of the product"),
            "productId": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the product"),
            "customerId": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the customer"),
            "category": openapi.Schema(type=openapi.TYPE_STRING, description="category of product"),
        },
    ),
    responses={200: openapi.Response("Item added to cart"), 400: "Invalid request"},
)

@api_view(["PATCH"])
def update_cart_item(request):
    """Update quantity of an item in the cart"""
    quantity = request.data.get("quantity", 1)
    product_id = request.data.get("productId")
    customer_id = request.data.get("customerId")
    category = request.data.get("category")
    try:
        cart = Cart.objects.get(customer_id=customer_id)
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id, product_type=category)
        product = get_product_by_url(category, product_id)
        # print(product)
        if check_product_stock(category, product_id, quantity):
            cart_item.quantity = quantity
            cart_item.price = product["price"]
            cart_item.save()
            update_product_stock(category, product_id, quantity)
            return Response({"message": "Cart item updated"})
        else:
            return Response({"error": "Insufficient stock"}, status=400)
    except CartItem.DoesNotExist:
        return Response({"error": "Item not found"}, status=404)

@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
       type=openapi.TYPE_OBJECT,
        required=["quantity", "productId", "customerId", "category"],  # Required fields
        properties={
            "quantity": openapi.Schema(type=openapi.TYPE_INTEGER, description="Quantity of the product"),
            "productId": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the product"),
            "customerId": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the customer"),
            "category": openapi.Schema(type=openapi.TYPE_STRING, description="category of product"),
        },
    ),
    responses={200: openapi.Response("Item added to cart"), 400: "Invalid request"},
)
@api_view(["POST"])
def add_to_cart(request):
    quantity = request.data.get("quantity", 1)
    customerId = request.data.get("customerId")
    productId = request.data.get("productId")
    category = request.data.get("category")

    if category not in ["books", "clothes", "phones"]:
        return Response({"error": "Invalid product type"}, status=400)

    if not check_product_stock(category, productId, quantity):
        return Response({"error": "Insufficient stock"}, status=400)

    cart, _ = Cart.objects.get_or_create(customer_id=customerId)

    product = get_product_by_url(category, productId)
    if not product:  # Ensure product exists
        return Response({"error": "Product not found"}, status=404)
    print(product)
    cartItem, created = CartItem.objects.get_or_create(
    cart=cart,
    product_id=productId,
    product_type=category,  # ✅ Ensure product uniqueness
    defaults={"quantity": quantity}
    )

    # Set additional fields
    cartItem.product_name = product["name"]
    cartItem.image_urls = product["url"]
    cartItem.price = product["price"]
    # print(cartItem)
    if not created:
        print("test")
        cartItem.quantity += quantity
        cartItem.product_type = category

    cartItem.save()

    update_product_stock(category, productId, quantity)

    cart_data = {
        "cart_id": cart.id,
        "customer_id": cart.customer_id,
        "items": [
            {"product_id": item.product_id, "quantity": item.quantity}
            for item in cart.items.all()
        ]
    }

    return Response({"message": "Item successfully added to cart", "cart": cart_data}, status=200)  # Corrected status
