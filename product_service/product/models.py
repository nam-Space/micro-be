from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    stock = models.IntegerField()
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


class Phone(Product):
    url = models.TextField(default="[]")
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    os = models.CharField(max_length=50)


class Clothes(Product):
    url = models.TextField(default="[]")
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=50)
    material = models.CharField(max_length=100)
