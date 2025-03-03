from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from .utils import check_product_stock, update_product_stock

@api_view(["GET"])
def get_cart(request, customer_id):
    """Retrieve cart details for a customer"""
    cart, created = Cart.objects.get_or_create(customer_id=customer_id)
    serializer = CartSerializer(cart)
    return Response(serializer.data)

@api_view(["POST"])
def add_to_cart(request, customer_id, product_id, product_type):
    """Add an item to the cart"""
    quantity = request.data.get("quantity", 1)
    if product_type not in ["books", "phones", "clothes"]:
        return Response({"error": "Invalid product type"}, status=400)

    if not check_product_stock(product_type, product_id, quantity):
        return Response({"error": "Insufficient stock"}, status=400)

    cart, _ = Cart.objects.get_or_create(customer_id=customer_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id, product_type=product_type)
    
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity

    cart_item.save()
    update_product_stock(product_type, product_id, quantity)

    return Response({"message": "Item added to cart"})

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

@api_view(["PUT"])
def update_cart_item(request, customer_id, product_id, product_type):
    """Update quantity of an item in the cart"""
    # quantity = request.data.get("quantity", 1)
    quantity = 2
    try:
        cart = Cart.objects.get(customer_id=customer_id)
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id, product_type=product_type)
        if check_product_stock(product_type, product_id, quantity):
            cart_item.quantity = quantity
            cart_item.save()
            update_product_stock(product_type, product_id, quantity)
            return Response({"message": "Cart item updated"})
        else:
            return Response({"error": "Insufficient stock"}, status=400)
    except CartItem.DoesNotExist:
        return Response({"error": "Item not found"}, status=404)

