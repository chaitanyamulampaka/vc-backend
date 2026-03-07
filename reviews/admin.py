from django.contrib import admin

# Register your models here.

from .models import Review, ReviewImage

class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    inlines = [ReviewImageInline]