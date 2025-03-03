from django.db import models

class Order(models.Model):
	customer_id = models.IntegerField()
	total_price = models.FloatField()
	created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
	order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
	product_type = models.CharField(max_length=255)
	product_id = models.IntegerField()
	quantity = models.IntegerField()
	price = models.FloatField()
