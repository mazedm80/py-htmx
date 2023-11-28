from typing import Dict, List, Optional

import httpx
from fastapi import Form

from config.settings import settings


API_HOST = settings.api.api_host


def get_restaurant_form_creds(
    name: str = Form(),
    address: str = Form(),
    phone: str = Form(),
    email: Optional[str] = Form(default=None),
    website: Optional[str] = Form(default=None),
    image: Optional[str] = Form(default=None),
) -> dict:
    image = "https://marketplace.canva.com/EAFYecj_1Sc/1/0/1600w/canva-cream-and-black-simple-elegant-catering-food-logo-2LPev1tJbrg.jpg"

    data = {
        "name": name,
        "address": address,
        "phone": phone,
        "email": email,
        "website": website,
        "image": image,
    }
    return data


async def get_restaurants(
    user_session: str,
) -> List:
    with httpx.Client() as client:
        try:
            response = client.get(
                f"{API_HOST}/restaurant",
                headers={"Authorization": f"Bearer {user_session}"},
            )
            response.raise_for_status()
            restaurants = response.json()["restaurants"]
            return restaurants
        except httpx.HTTPStatusError as exc:
            return exc.response.status_code


async def get_restaurant(
    restaurant_id: int,
    user_session: str,
) -> Dict:
    with httpx.Client() as client:
        try:
            response = client.get(
                f"{API_HOST}/restaurant",
                headers={"Authorization": f"Bearer {user_session}"},
                params={"restaurant_id": restaurant_id},
            )
            response.raise_for_status()
            restaurant = response.json()["restaurants"][0]
            return restaurant
        except httpx.HTTPStatusError as exc:
            return exc.response.status_code


async def add_restaurant(
    data: dict,
    user_session: str,
) -> int:
    with httpx.Client() as client:
        try:
            response = client.post(
                f"{API_HOST}/restaurant",
                headers={"Authorization": f"Bearer {user_session}"},
                json=data,
            )
            response.raise_for_status()
            return response.status_code
        except httpx.HTTPStatusError as exc:
            return exc.response.status_code


async def update_restaurant(
    data: dict,
    restaurant_id: int,
    user_session: str,
) -> int:
    with httpx.Client() as client:
        try:
            data["id"] = restaurant_id
            print(data)
            response = client.put(
                f"{API_HOST}/restaurant",
                headers={"Authorization": f"Bearer {user_session}"},
                json=data,
            )
            response.raise_for_status()
            return response.status_code
        except httpx.HTTPStatusError as exc:
            return exc.response.status_code


async def delete_restaurant(
    restaurant_id: int,
    user_session: str,
) -> int:
    with httpx.Client() as client:
        try:
            response = client.delete(
                f"{API_HOST}/restaurant",
                headers={"Authorization": f"Bearer {user_session}"},
                params={"restaurant_id": restaurant_id},
            )
            response.raise_for_status()
            return response.status_code
        except httpx.HTTPStatusError as exc:
            return exc.response.status_code
