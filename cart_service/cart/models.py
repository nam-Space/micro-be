from django.db import models

class Cart(models.Model):
    customer_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product_id = models.IntegerField()
    product_type = models.CharField(max_length=20)  # "books", "phones", "clothes"
    quantity = models.PositiveIntegerField(default=1)
