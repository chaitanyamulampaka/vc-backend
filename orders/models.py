from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User
from products.models import Product

from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    # Payment
    is_paid = models.BooleanField(default=False)

    # Order Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # 🔥 Amount Breakdown
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    shipping_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # Shipping Details (Snapshot copy)
    full_name = models.CharField(max_length=150)
    mobile = models.CharField(max_length=15)
    address_line = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    # Courier Details
    courier_name = models.CharField(max_length=100, null=True, blank=True)
    courier_id = models.IntegerField(null=True, blank=True)

    # Shiprocket Fields
    shiprocket_order_id = models.CharField(max_length=100, null=True, blank=True)
    shipment_id = models.CharField(max_length=100, null=True, blank=True)
    tracking_number = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # 🔥 Automatically calculate total
        self.total_amount = self.subtotal + self.shipping_cost
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
from products.models import Product

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    # Store price at purchase time (VERY IMPORTANT)
    price_at_purchase = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"