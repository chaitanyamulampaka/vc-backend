from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services.shiprocket import check_serviceability


@api_view(["GET"])
def shipping_options(request):
    delivery_pincode = request.GET.get("delivery_pincode")
    payment_mode = request.GET.get("payment_mode")  # "cod" or "prepaid"

    pickup_pincode = "531082"

    cod_value = 1 if payment_mode == "cod" else 0

    data = check_serviceability(
        pickup_pincode,
        delivery_pincode,
        weight=0.3,
        cod=cod_value
    )

    couriers = []
    print("Shiprocket full response:", data)
    for courier in data.get("data", {}).get("available_courier_companies", []):
        couriers.append({
            "courier_name": courier["courier_name"],
            "courier_id": courier["courier_company_id"],
            "rate": courier["rate"],
            "estimated_days": courier["estimated_delivery_days"],
            "rating": courier.get("rating", 4)
        })

    return Response(couriers)

from decimal import Decimal
from rest_framework.decorators import api_view
from rest_framework.response import Response
from cart.models import Cart
from .models import Order, OrderItem
from accounts.models import Address
from cart.models import Cart
from decimal import Decimal
from django.db import transaction


@api_view(["POST"])
def create_order(request):

    user = request.user
    address_id = request.data.get("address_id")
    courier_id = request.data.get("courier_id")
    courier_name = request.data.get("courier_name")
    shipping_cost = Decimal(request.data.get("shipping_cost", 0))
    payment_mode = request.data.get("payment_mode")

    cart = Cart.objects.get(user=user)

    if not cart.items.exists():
        return Response({"error": "Cart is empty"}, status=400)

    subtotal = Decimal(0)

    for item in cart.items.all():

        product = item.product

        # 🔥 Check stock
        if product.stock < item.quantity:
            return Response(
                {"error": f"{product.name} is out of stock"},
                status=400
            )

        subtotal += Decimal(product.cost) * item.quantity

    address = user.addresses.get(id=address_id)

    with transaction.atomic():

        order = Order.objects.create(
            user=user,
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            full_name=address.full_name,
            mobile=address.mobile,
            address_line=address.address_line,
            city=address.city,
            state=address.state,
            pincode=address.pincode,
            courier_id=courier_id,
            courier_name=courier_name,
            status="pending",
            is_paid=False
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_at_purchase=item.product.cost
            )

        # 🔥 If COD → clear cart immediately
        if payment_mode == "cod":

            for item in order.items.all():
                product = item.product
                product.stock -= item.quantity
                product.save()

            cart.items.all().delete()
    return Response({
        "id": order.id,
        "total_amount": order.total_amount
    })

    from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from .models import Order


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_orders(request):

    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    data = []

    for order in orders:

        items = []

        for item in order.items.all():
            items.append({
                "product_name": item.product.name,
                "quantity": item.quantity,
                "price": item.price_at_purchase,
            })

        data.append({
            "id": order.id,
            "status": order.status,
            "is_paid": order.is_paid,
            "total_amount": order.total_amount,
            "created_at": order.created_at,
            "tracking_number": order.tracking_number,
            "items": items
        })

    return Response(data)