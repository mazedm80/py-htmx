from typing import Dict, List, Optional, Any, Tuple

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
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{API_HOST}/order",
                headers={"Authorization": f"Bearer {user_session}"},
                params={"restaurant_id": data["restaurant_id"]},
                json=order,
            )
            response.raise_for_status()
            order_id = response.json()
            if order_id:
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
                    response = await client.post(
                        f"{API_HOST}/order/order_details",
                        headers={"Authorization": f"Bearer {user_session}"},
                        params={"order_id": order_id},
                        json=items,
                    )
                    response.raise_for_status()
                except httpx.HTTPError as e:
                    print(e)
                    response = None
        except httpx.HTTPError as e:
            print(e)
            response = None
    return response.status_code


async def update_order_status(
    status: Optional[str],
    payment_status: Optional[str],
    order_id: str,
    user_session: str,
) -> int:
    if status:
        params = {"status": status, "order_id": order_id}
    elif payment_status:
        params = {"payment_status": payment_status, "order_id": order_id}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(
                f"{API_HOST}/order/status",
                headers={"Authorization": f"Bearer {user_session}"},
                params=params,
            )
            response.raise_for_status()
        except httpx.HTTPError as e:
            print(e)
            response = None
    return response.status_code


async def get_order_by_status(
    status: Optional[str],
    payment_status: Optional[str],
    user_session: str,
) -> Tuple[List[Dict[str, Any]]]:
    if status:
        params = {"status": status, "restaurant_id": 2}
    elif payment_status:
        params = {"payment_status": payment_status, "restaurant_id": 2}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{API_HOST}/order/by_status",
                headers={"Authorization": f"Bearer {user_session}"},
                params=params,
            )
            response.raise_for_status()
            orders = response.json()
        except httpx.HTTPError:
            orders = []
    return orders


async def get_order_details_by_id(
    order_id: str,
    user_session: str,
) -> Tuple[Dict[str, Any]]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{API_HOST}/order/details",
                headers={"Authorization": f"Bearer {user_session}"},
                params={"order_id": order_id},
            )
            response.raise_for_status()
            order = response.json()
        except httpx.HTTPError:
            order = {}
        try:
            response = await client.get(
                f"{API_HOST}/order/order_details",
                headers={"Authorization": f"Bearer {user_session}"},
                params={"order_id": order_id},
            )
            response.raise_for_status()
            order_details = response.json()
        except httpx.HTTPError:
            order_details = []
    return order, order_details
