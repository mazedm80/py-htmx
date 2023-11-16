from typing import Optional

import httpx
from fastapi import Depends, Form

from app.utils.auth import UserSession, get_user_session
from config.settings import settings


def get_menu_form_creds(
    name: str = Form(),
    price: float = Form(),
    description: str = Form(),
    making_time: str = Form(),
    spice_level: str = Form(),
    vegetarian: bool = Form(),
    vegan: bool = Form(),
    gluten_free: bool = Form(),
    status: str = Form(),
    session: Optional[UserSession] = Depends(get_user_session),
) -> int:
    image = "https://pngfre.com/wp-content/uploads/Burger-43.png"
    status = True if status == "Available" else False
    data = {
        "menu_category_id": 1,
        "name": name,
        "description": description,
        "price": price,
        "making_time": making_time.replace(":", "."),
        "image": str(image),
        "status": status,
        "spice_level": spice_level.lower(),
        "vegetarian": vegetarian,
        "vegan": vegan,
        "gluten_free": gluten_free,
    }
    with httpx.Client() as client:
        try:
            response = client.post(
                f"{settings.api_host}/menu",
                headers={"Authorization": f"Bearer {session.user_session}"},
                json=data,
            )
            response.raise_for_status()
        except httpx.HTTPError:
            response = None
        print(response.status_code)
    return response.status_code
