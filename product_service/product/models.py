from django.db import models

# Create your models here.
from djongo import models

# ✅ Abstract base class (acts like an interface)
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  

    def __str__(self):
        return self.name

# ✅ Concrete product models inheriting from Product
class Book(Product):
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)

class Phone(Product):
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    os = models.CharField(max_length=50)

class Clothes(Product):
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=50)
    material = models.CharField(max_length=100)
