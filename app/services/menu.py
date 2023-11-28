from typing import Dict, List, Optional

import httpx
from fastapi import Form

from config.settings import settings


API_HOST = settings.api.api_host


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
    status = True if status == "available" else False
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


def get_menu_category_form_creds(
    name: str = Form(),
    description: Optional[str] = Form(default=None),
) -> dict:
    image = "https://pngfre.com/wp-content/uploads/Burger-43.png"
    data = {
        "name": name,
        "description": description,
        "image": str(image),
    }
    return data


async def get_menu_items(
    user_session: str,
    category_id: Optional[int] = None,
) -> List:
    with httpx.Client() as client:
        try:
            if category_id:
                response = client.get(
                    f"{API_HOST}/menu",
                    headers={"Authorization": f"Bearer {user_session}"},
                    params={"category_id": category_id},
                )
            else:
                response = client.get(
                    f"{API_HOST}/menu",
                    headers={"Authorization": f"Bearer {user_session}"},
                )
            response.raise_for_status()
            menu_list = response.json()
        except httpx.HTTPError as e:
            print(e)
            menu_list = []
    return menu_list


async def get_menu_item(
    menu_id: int,
    user_session: str,
) -> dict:
    with httpx.Client() as client:
        try:
            response = client.get(
                f"{API_HOST}/menu",
                headers={"Authorization": f"Bearer {user_session}"},
                params={"menu_id": menu_id},
            )
            response.raise_for_status()
            item = response.json()[0]
            if item.get("vegetarian"):
                item["vegetarian"] = "yes"
            else:
                item["vegetarian"] = "no"
            if item.get("vegan"):
                item["vegan"] = "yes"
            else:
                item["vegan"] = "no"
            if item.get("gluten_free"):
                item["gluten_free"] = "yes"
            else:
                item["gluten_free"] = "no"
            if item.get("status"):
                item["status"] = "available"
            else:
                item["status"] = "unavailable"
        except httpx.HTTPError:
            item = {}
    return item


async def add_menu_item(
    data: dict,
    user_session: str,
) -> int:
    with httpx.Client() as client:
        try:
            response = client.post(
                f"{API_HOST}/menu",
                headers={"Authorization": f"Bearer {user_session}"},
                json=data,
            )
            response.raise_for_status()
        except httpx.HTTPError:
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
                f"{API_HOST}/menu",
                headers={"Authorization": f"Bearer {user_session}"},
                json=data,
            )
            response.raise_for_status()
        except httpx.HTTPError:
            response = None
    return response.status_code


async def delete_menu_item(
    menu_id: int,
    user_session: str,
) -> int:
    with httpx.Client() as client:
        try:
            response = client.delete(
                f"{API_HOST}/menu",
                headers={"Authorization": f"Bearer {user_session}"},
                params={"menu_id": menu_id},
            )
            response.raise_for_status()
        except httpx.HTTPError:
            response = None
    return response.status_code


async def get_menu_categories(
    user_session: str,
) -> List[Dict]:
    with httpx.Client() as client:
        try:
            response = client.get(
                f"{API_HOST}/menu/categories",
                headers={"Authorization": f"Bearer {user_session}"},
            )
            response.raise_for_status()
            menu_categories = response.json()
            options = []
            for category in menu_categories:
                options.append(
                    {
                        "value": category["id"],
                        "name": category["name"],
                        "description": category["description"],
                        "image": category["image"],
                    }
                )
        except httpx.HTTPError as e:
            print(e)
            options = []
    return options


async def get_menu_category(
    category_id: int,
    user_session: str,
) -> dict:
    with httpx.Client() as client:
        try:
            response = client.get(
                f"{API_HOST}/menu/category",
                headers={"Authorization": f"Bearer {user_session}"},
                params={"category_id": category_id},
            )
            response.raise_for_status()
            menu_category = response.json()
        except httpx.HTTPError:
            menu_category = {}
    return menu_category


async def add_menu_category(
    data: dict,
    user_session: str,
) -> int:
    with httpx.Client() as client:
        try:
            response = client.post(
                f"{API_HOST}/menu/category",
                headers={"Authorization": f"Bearer {user_session}"},
                json=data,
            )
            response.raise_for_status()
        except httpx.HTTPError:
            response = None
    return response.status_code


async def update_menu_category(
    data: dict,
    category_id: int,
    user_session: str,
) -> int:
    with httpx.Client() as client:
        try:
            data["id"] = category_id
            response = client.put(
                f"{API_HOST}/menu/category",
                headers={"Authorization": f"Bearer {user_session}"},
                json=data,
            )
            response.raise_for_status()
        except httpx.HTTPError:
            response = None
    return response.status_code


async def delete_menu_category(
    category_id: int,
    user_session: str,
) -> int:
    with httpx.Client() as client:
        try:
            response = client.delete(
                f"{API_HOST}/menu/category",
                headers={"Authorization": f"Bearer {user_session}"},
                params={"category_id": category_id},
            )
            response.raise_for_status()
        except httpx.HTTPError:
            response = None
    return response.status_code
