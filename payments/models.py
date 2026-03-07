from django.db import models
from django.db import models
from orders.models import Order

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=200)
    razorpay_payment_id = models.CharField(max_length=200, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="created")
    created_at = models.DateTimeField(auto_now_add=True)
# Create your models here.
