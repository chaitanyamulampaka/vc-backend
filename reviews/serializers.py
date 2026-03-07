from rest_framework import serializers

from .models import Review,  ReviewImage

class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ["id", "image"]

class ReviewSerializer(serializers.ModelSerializer):
    images = ReviewImageSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "product",
            "rating",
            "comment",
            "is_verified_purchase",
            "created_at",
            "images",
        ]
        read_only_fields = ["user", "created_at"]