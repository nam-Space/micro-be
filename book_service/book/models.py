from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    stock = models.IntegerField()
    score = models.FloatField(default=0.0)
    # ✅ Add this field explicitly
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # ✅ Abstract class (no table)

    def __str__(self):
        return self.name


class Book(Product):
    url = models.TextField(default="[]")
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
