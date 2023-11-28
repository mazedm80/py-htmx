from typing import Dict, List, Optional

import httpx

from config.settings import settings


API_HOST = settings.api.api_host


async def post_order(
    data: dict,
    user_session: str,
) -> int:
    order = {
        "order_id": data["order_id"],
        "user_id": data["user_id"],
        "table_number": data["table_number"],
        "status": data["status"],
        "order_type": data["order_type"],
        "payment_status": data["payment_status"],
        "total_amount": data["total"],
        "coupon_code": data["coupon_code"],
        "note": data["note"],
    }
    with httpx.Client() as client:
        try:
            response = client.post(
                f"{API_HOST}/order",
                headers={"Authorization": f"Bearer {user_session}"},
                params={"restaurant_id": data["restaurant_id"]},
                json=order,
            )
            response.raise_for_status()
            order_id = response.json()
        except httpx.HTTPError:
            response = None
        try:
            items = []
            for item in data["items"]:
                items.append(
                    {
                        "menu_item_id": item["menu_item_id"],
                        "quantity": item["quantity"],
                        "price": item["price"],
                    }
                )
            response = client.post(
                f"{API_HOST}/order/order_details",
                headers={"Authorization": f"Bearer {user_session}"},
                params={"order_id": order_id},
                json=items,
            )
            response.raise_for_status()
        except httpx.HTTPError:
            response = None
    return response.status_code
