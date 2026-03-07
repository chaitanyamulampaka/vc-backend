from django.contrib import admin
from .models import Product, ProductImage, ProductFeature, ArtistProduct


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "cost", "stock", "artist", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name",)
    inlines = [ProductImageInline, ProductFeatureInline]

from .models import ArtistProductImage

class ArtistProductImageInline(admin.TabularInline):
    model = ArtistProductImage
    extra = 1

@admin.register(ArtistProduct)
class ArtistProductAdmin(admin.ModelAdmin):
    inlines = [ArtistProductImageInline]