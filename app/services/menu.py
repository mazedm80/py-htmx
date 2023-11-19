from typing import Optional

import httpx
from fastapi import Depends, Form

from app.utils.auth import UserSession, get_user_session
from config.settings import settings


def get_menu_form_creds(
    name: str = Form(),
    price: int = Form(),
    description: Optional[str] = Form(default=None),
    making_time: int = Form(),
    spice_level: str = Form(),
    vegetarian: bool = Form(),
    vegan: bool = Form(),
    gluten_free: bool = Form(),
    status: str = Form(),
) -> dict:
    image = "https://pngfre.com/wp-content/uploads/Burger-43.png"
    status = True if status == "Available" else False
    data = {
        "menu_category_id": 1,
        "name": name,
        "description": description,
        "price": price,
        "making_time": making_time,
        "image": str(image),
        "status": status,
        "spice_level": spice_level.lower(),
        "vegetarian": vegetarian,
        "vegan": vegan,
        "gluten_free": gluten_free,
    }
    return data


async def get_menu_item(
    menu_id: int,
    user_session: str,
) -> dict:
    with httpx.Client() as client:
        try:
            response = client.get(
                f"{settings.api_host}/menu",
                headers={"Authorization": f"Bearer {user_session}"},
                params={"menu_id": menu_id},
            )
            response.raise_for_status()
            item = response.json()["menu_items"][0]
        except httpx.HTTPError as e:
            item = {}
    return item


async def add_menu_item(
    data: dict,
    user_session: str,
) -> int:
    with httpx.Client() as client:
        try:
            response = client.post(
                f"{settings.api_host}/menu",
                headers={"Authorization": f"Bearer {user_session}"},
                json=data,
            )
            response.raise_for_status()
        except httpx.HTTPError as e:
            response = None
    return response.status_code


async def update_menu_item(
    data: dict,
    menu_id: int,
    user_session: str,
) -> int:
    with httpx.Client() as client:
        try:
            data["id"] = menu_id
            response = client.put(
                f"{settings.api_host}/menu",
                headers={"Authorization": f"Bearer {user_session}"},
                json=data,
            )
            response.raise_for_status()
        except httpx.HTTPError as e:
            response = None
    return response.status_code


async def delete_menu_item(
    menu_id: int,
    user_session: str,
) -> int:
    with httpx.Client() as client:
        try:
            response = client.delete(
                f"{settings.api_host}/menu",
                headers={"Authorization": f"Bearer {user_session}"},
                params={"menu_id": menu_id},
            )
            response.raise_for_status()
        except httpx.HTTPError as e:
            response = None
    return response.status_code
