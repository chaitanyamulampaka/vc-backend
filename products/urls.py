from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet,
    ArtistProductViewSet,
    AdminArtistProductViewSet
)

router = DefaultRouter()

router.register('products', ProductViewSet, basename='products')
router.register('artist/products', ArtistProductViewSet, basename='artist-products')
router.register('admin/artist-products', AdminArtistProductViewSet, basename='admin-artist-products')

urlpatterns = [
    path('', include(router.urls)),
]