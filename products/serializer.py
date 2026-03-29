from rest_framework import serializers
from .models import (
    Product,
    ProductImage,
    ProductFeature,
    ArtistProduct,
    ArtistProductImage
)

# ───────── PRODUCT ─────────
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image"]


class ProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = ["id", "title"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    features = ProductFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


# ───────── ARTIST PRODUCT ─────────
class ArtistProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistProductImage
        fields = ["id", "image"]
    def get_image(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url

class ArtistProductSerializer(serializers.ModelSerializer):
    images = ArtistProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = ArtistProduct
        fields = "__all__"
        read_only_fields = ["artist", "status"]