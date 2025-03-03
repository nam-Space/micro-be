from django.db import models
from django.contrib.auth.models import AbstractUser

# Extend Django's built-in User model
class Customer(AbstractUser):
    CUSTOMER_TYPES = [
        ('regular', 'Regular Customer'),
        ('business', 'Business Customer'),
        ('premium', 'Premium Customer'),
    ]
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPES)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)

    # ✅ Fix conflicts by setting related_name for groups & permissions
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customer_users",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customer_users",
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.customer_type})"


# Address model linked to Customer
class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="addresses")
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"

# Account model linked to Customer
class Account(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="account")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    account_status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')

    def __str__(self):
        return f"Account of {self.customer.username} - Balance: {self.balance}"
