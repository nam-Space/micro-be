# comment/models.py
from django.db import models
import uuid


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.IntegerField()
    username = models.CharField(max_length=255)
    product_id = models.IntegerField()
    category = models.CharField(max_length=50)  # book, phone, clothes
    content = models.TextField()
    sentiment = models.CharField(max_length=20, null=True, blank=True)
    confidence = models.FloatField(null=True, blank=True)  # ← Thêm trường này
    created_at = models.DateTimeField(auto_now_add=True)
