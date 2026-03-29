from rest_framework import serializers
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_price = serializers.DecimalField(
        source="product.cost",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    product_image = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ["id", "product", "product_name", "product_price","product_image", "quantity"]

    def get_product_image(self, obj):
        request = self.context.get('request')
        # Check if product has an image
        if obj.product.img:
            image_url = obj.product.img.url
            # If request is available, return absolute URL (http://127.0.0.1:8000/media/...)
            if request is not None:
                return request.build_absolute_uri(image_url)
            return image_url
        return None
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "items"]
        read_only_fields = ["user"]