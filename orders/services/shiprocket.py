import requests
from django.conf import settings

BASE_URL = "https://apiv2.shiprocket.in/v1/external"

def get_shiprocket_token():
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": settings.SHIPROCKET_EMAIL,
            "password": settings.SHIPROCKET_PASSWORD
        }
    )

    print("Login status:", response.status_code)
    print("Login response:", response.text)

    data = response.json()
    return data.get("token")
def check_serviceability(pickup_pincode, delivery_pincode, weight=0.3, cod=0):
    token = get_shiprocket_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f"{BASE_URL}/courier/serviceability/",
        headers=headers,
        params={
            "pickup_postcode": pickup_pincode,
            "delivery_postcode": delivery_pincode,
            "weight": weight,
            "cod": cod
        }
    )

    return response.json()


def create_shiprocket_order(order, courier_id):
    token = get_shiprocket_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "order_id": str(order.id),
        "order_date": str(order.created_at),
        "pickup_location": "Primary",
        "billing_customer_name": order.full_name,
        "billing_address": order.address_line,
        "billing_city": order.city,
        "billing_pincode": order.pincode,
        "billing_state": order.state,
        "billing_country": "India",
        "billing_phone": order.mobile,
        "order_items": [
            {
                "name": item.product.name,
                "sku": str(item.product.id),
                "units": item.quantity,
                "selling_price": item.price_at_purchase
            }
            for item in order.items.all()
        ],
        "payment_method": "Prepaid",
        "sub_total": order.total_amount,
        "courier_id": courier_id
    }

    response = requests.post(
        f"{BASE_URL}/orders/create/adhoc",
        headers=headers,
        json=payload
    )

    return response.json()