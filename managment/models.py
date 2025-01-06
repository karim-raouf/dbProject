from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission



class User(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='ecommerce_user_set',  # Add a custom related_name here
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='ecommerce_user_permissions_set',  # Add a custom related_name here
        blank=True
    )
    
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Supplier', 'Supplier'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.username} ({self.role})"


class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='supplier_profile',null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name


class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory')
    stock_level = models.IntegerField()
    low_stock_alert = models.IntegerField(default=10)  # Default alert threshold

    def __str__(self):
        return f"{self.product.name} - {self.location}"


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='orders')
    quantity = models.IntegerField()
    order_date = models.DateField(auto_now_add=True)
    received_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Received', 'Received')],
        default='Pending',
    )

    def __str__(self):
        return f"Order {self.id} - {self.product.name}"

