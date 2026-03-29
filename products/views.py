from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import ArtistProductImage, Product, ProductImage
from .serializer import ProductImageSerializer, ProductSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics,mixins,viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.views import APIView
class ProductViewSet(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    permission_classes = [IsAuthenticated]
    @action(detail=True, methods=['get'])
    def images(self, request, pk=None):
        product = self.get_object()
        images = product.images.all()
        serializer = ProductImageSerializer(images, many=True , context={'request': request})
        return Response(serializer.data)


    
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsArtist
from .models import ArtistProduct
from .serializer import ArtistProductSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ArtistProduct, ArtistProductImage
from .serializer import ArtistProductSerializer


class ArtistProductViewSet(viewsets.ModelViewSet):
    serializer_class = ArtistProductSerializer
    permission_classes = [IsArtist]

    def get_queryset(self):
        # 🔥 Only return current artist's products
        return ArtistProduct.objects.filter(artist=self.request.user)

    def perform_create(self, serializer):
        artist_product = serializer.save(
            artist=self.request.user,
            status="pending"
        )

        # 🔥 Handle multiple images
        images = self.request.FILES.getlist("images")
        for image in images:
            ArtistProductImage.objects.create(
                artist_product=artist_product,
                image=image
            )

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import Product
from .models import ProductFeature
from django.db import transaction
class AdminArtistProductViewSet(viewsets.ModelViewSet):
    queryset = ArtistProduct.objects.all()
    serializer_class = ArtistProductSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        artist_product = self.get_object()

        if artist_product.status == "approved":
            return Response({"error": "Already approved"}, status=400)

        try:
            # 🛡️ Wrap in a transaction to prevent partial data creation
            with transaction.atomic():
                # 1. Create the main Product
                product = Product.objects.create(
                    name=artist_product.name,
                    cost=artist_product.cost,
                    discount=artist_product.discount,
                    oldprice=artist_product.oldprice,
                    stock=artist_product.stock,
                    rating=artist_product.rating,
                    # Description was missing in your previous create call but exists in ArtistProduct
                    # Ensure your Product model has a description field if you want to save it!
                    img=artist_product.images.first().image if artist_product.images.exists() else None,
                    artist=artist_product.artist
                )

                # 2. Copy images
                for artist_img in artist_product.images.all():
                    ProductImage.objects.create(
                        product=product,
                        image=artist_img.image
                    )

                # 3. Copy features (FIXED FIELD NAME HERE)
                if artist_product.features:
                    # Split by comma and strip whitespace
                    features_list = artist_product.features.split(",")
                    for f_text in features_list:
                        if f_text.strip(): # Avoid empty strings
                            ProductFeature.objects.create(
                                product=product,
                                title=f_text.strip()  # ✅ Changed 'feature' to 'title'
                            )

                # 4. Update status
                artist_product.status = "approved"
                artist_product.save()

            return Response({"message": "Product approved successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Approval failed: {str(e)}"}, status=500)
    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        artist_product = self.get_object()

        if artist_product.status == "rejected":
            return Response(
                {"error": "Already rejected"},
                status=status.HTTP_400_BAD_REQUEST
            )

        artist_product.status = "rejected"
        artist_product.save()

        return Response({"message": "Product rejected successfully"})
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "role": request.user.profile.role,
            "is_staff": request.user.is_staff
        })