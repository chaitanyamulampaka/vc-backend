import razorpay
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from orders.models import Order
from .models import Payment

class CreateRazorpayOrder(APIView):

    def post(self, request):
        order_id = request.data.get("order_id")
        order = Order.objects.get(id=order_id)

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        razorpay_order = client.order.create({
            "amount": int(order.total_amount * 100),
            "currency": "INR"
        })

        Payment.objects.create(
            order=order,
            razorpay_order_id=razorpay_order["id"],
            amount=order.total_amount
        )

        return Response({
            "razorpay_order_id": razorpay_order["id"],
            "key": settings.RAZORPAY_KEY_ID,
            "amount": razorpay_order["amount"]
        })
from django.conf import settings
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response

import razorpay

from cart.models import Cart
from products.models import Product
from .models import Payment


class VerifyPayment(APIView):

    def post(self, request):

        razorpay_order_id = request.data.get("razorpay_order_id")
        razorpay_payment_id = request.data.get("razorpay_payment_id")
        razorpay_signature = request.data.get("razorpay_signature")

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        try:
            # 🔐 Verify Razorpay signature
            client.utility.verify_payment_signature({
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature
            })

            payment = Payment.objects.get(
                razorpay_order_id=razorpay_order_id
            )

            order = payment.order

            # 🔥 Prevent duplicate verification
            if order.is_paid:
                return Response({"message": "Order already paid"})

            with transaction.atomic():

                # Update payment record
                payment.status = "success"
                payment.razorpay_payment_id = razorpay_payment_id
                payment.razorpay_signature = razorpay_signature
                payment.save()

                # Update order status
                order.is_paid = True
                order.status = "paid"
                order.save()

                # 🔒 Lock products & reduce stock safely
                for item in order.items.select_related("product"):

                    product = Product.objects.select_for_update().get(
                        id=item.product.id
                    )

                    if product.stock < item.quantity:
                        raise Exception(
                            f"{product.name} stock insufficient"
                        )

                    product.stock -= item.quantity
                    product.save()

                # 🧹 Clear user's cart
                try:
                    cart = Cart.objects.get(user=order.user)
                    cart.items.all().delete()
                except Cart.DoesNotExist:
                    pass

            return Response({
                "message": "Payment verified, stock updated, cart cleared"
            })

        except Exception as e:
            return Response(
                {
                    "message": "Verification failed",
                    "error": str(e)
                },
                status=400
            )