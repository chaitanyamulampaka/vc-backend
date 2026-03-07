from django.urls import path
from .views import create_order, my_orders, shipping_options

urlpatterns = [
    path("shipping/options/", shipping_options),
    path("create/", create_order),
    path("my-orders/", my_orders),
]
