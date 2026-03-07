from django.urls import path
from .views import CreateRazorpayOrder, VerifyPayment

urlpatterns = [
    path("create-order/", CreateRazorpayOrder.as_view()),
    path("verify/", VerifyPayment.as_view()),
]