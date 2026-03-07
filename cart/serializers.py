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

    class Meta:
        model = CartItem
        fields = ["id", "product", "product_name", "product_price", "quantity"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "items"]
        read_only_fields = ["user"]