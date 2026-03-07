from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "product")  # One review per user per product

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating})"


class ReviewImage(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(upload_to="review_images/")

    def __str__(self):
        return f"Image for Review {self.review.id}"