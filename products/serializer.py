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
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj.image:
            return obj.image.url  # ✅ Returns full Cloudinary URL
        return None

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
    img = serializers.SerializerMethodField()

    def get_img(self, obj):
        if obj.img:
            return obj.img.url  # ✅ Returns full Cloudinary URL
        return None

    class Meta:
        model = Product
        fields = "__all__"


# ───────── ARTIST PRODUCT ─────────
class ArtistProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):  # ✅ Now actually connected
        if obj.image:
            return obj.image.url
        return None

    class Meta:
        model = ArtistProductImage
        fields = ["id", "image"]


class ArtistProductSerializer(serializers.ModelSerializer):
    images = ArtistProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = ArtistProduct
        fields = "__all__"
        read_only_fields = ["artist", "status"]