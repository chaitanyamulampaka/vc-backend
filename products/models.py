from django.db import models

from django.contrib.auth.models import User

class Product(models.Model): 
    name = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2) 
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    oldprice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rating = models.IntegerField(default=0, choices=[(i, i) for i in range(1, 6)])
    stock = models.IntegerField(default=0)
    img = models.ImageField(upload_to="product_imgs/", null=True, blank=True) 

    # 🔥 NEW FIELD
    artist = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_products"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images' 
    )
    image = models.ImageField(upload_to='product_imgs/')
    

    def __str__(self):
        return f"Image for {self.product.name}"

class ProductFeature(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='features'
    )
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    

from django.db import models
from django.contrib.auth.models import User

class ArtistProduct(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    artist = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    oldprice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(default=0)
    rating = models.IntegerField(default=1)

    
    features = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)


class ArtistProductImage(models.Model):
    artist_product = models.ForeignKey(
        "ArtistProduct",
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="artist_products/")

    def __str__(self):
        return f"Image for {self.artist_product.name}"