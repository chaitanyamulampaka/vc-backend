from rest_framework import serializers
from .models import ArtistProductImage, Product,ProductFeature,ProductImage,ArtistProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'
    
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields='__all__'
    
class ProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductFeature
        fields='__all__'
        


class ArtistProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistProductImage
        fields = ["id", "image"]
class ArtistProductSerializer(serializers.ModelSerializer):
    images = ArtistProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = ArtistProduct
        fields = "__all__"
        read_only_fields = ["artist", "status"]   # 🔥 ADD THIS