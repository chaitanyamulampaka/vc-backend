from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.db import transaction

from .models import Cart, CartItem
from .serializers import CartSerializer
from products.models import Product


class CartViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart,context={'request': request})
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request):
        product_id = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))

        cart, created = Cart.objects.get_or_create(user=request.user)

        product = Product.objects.get(pk=product_id)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not created:
            item.quantity += quantity
            if item.quantity <= 0:
                item.delete()
                return Response({"message": "Item removed"})
        else:
            item.quantity = quantity
        item.save()

        return Response({"message": "Product added to cart"})
    @transaction.atomic
    def destroy(self, request, pk=None):
        item = CartItem.objects.get(pk=pk, cart__user=request.user)
        item.delete()
        return Response({"message": "Item removed"})