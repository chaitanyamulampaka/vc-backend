from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "is_paid", "total_amount", "created_at")
    list_filter = ("is_paid", "created_at")
    search_fields = ("user__username",)
    inlines = [OrderItemInline]