from django.db import models
import uuid

class PaymentStatus(models.TextChoices):
    PENDING = "Pending", "Pending"
    SUCCESS = "Success", "Success"
    FAILED = "Failed", "Failed"

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_id = models.UUIDField()  # Reference Order from Order API
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50, default="PayPal")
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
