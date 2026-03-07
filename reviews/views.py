from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from rest_framework import serializers
from .models import Review, ReviewImage
from .serializers import ReviewSerializer
from orders.models import OrderItem  # assuming you have this


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        product_id = self.request.query_params.get("product")
        queryset = Review.objects.all()

        if product_id:
            queryset = queryset.filter(product_id=product_id)
        
        return queryset


    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user
        product = serializer.validated_data["product"]

        # 🔹 Check duplicate review
        if Review.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError(
                "You have already reviewed this product."
            )

        # 🔹 Check verified purchase (basic logic)
        is_verified = OrderItem.objects.filter(
            order__user=user,
            product=product,
            order__is_paid=True
        ).exists()

        review = serializer.save(
            user=user,
            is_verified_purchase=is_verified
        )

        # 🔹 Handle images
        images = self.request.FILES.getlist("images")

        for image in images:
            ReviewImage.objects.create(
                review=review,
                image=image
            )

    @transaction.atomic
    def perform_update(self, serializer):
        review = serializer.save()

        # Optional: replace images on update
        images = self.request.FILES.getlist("images")

        if images:
            review.images.all().delete()
            for image in images:
                ReviewImage.objects.create(
                    review=review,
                    image=image
                )