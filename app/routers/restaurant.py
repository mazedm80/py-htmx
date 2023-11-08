from typing import Optional

import httpx
from fastapi import APIRouter, Depends, Request, status, Response
from fastapi.responses import HTMLResponse

from app import templates
from app.utils.auth import Token, get_userinfo_for_page
from app.utils.exceptions import UnauthorizedPageException
from config.settings import settings

router = APIRouter(
    prefix="/restaurant",
    tags=["restaurant"],
)


@router.get(
    path="",
    summary="Gets the restaurant page.",
    tags=["Pages"],
    response_class=HTMLResponse,
)
async def get_dashboard(
    request: Request,
    # cookie: Optional[Token] = Depends(get_auth_cookie),
    cookie: int = 1,
):
    restaurant_list = []
    for i in range(1, 4):
        restaurant_list.append(
            {
                "id": i,
                "name": f"Restaurant{i}",
                "address": "1234 Main St.",
                "phone": "123-456-7890",
                "email": "abc@abc.com",
                "website": "https://www.google.com",
                "image": "https://via.placeholder.com/150",
            }
        )
    title = "Restaurant"
    context = {"request": request, "restaurant_list": restaurant_list, "title": title}
    if not cookie:
        raise UnauthorizedPageException()
    return templates.TemplateResponse("pages/restaurant.html", context)


@router.delete(
    path="/{restaurant_id}",
    summary="Deletes a restaurant.",
    tags=["Restaurant"],
)
async def delete_restaurant(
    restaurant_id: int,
    # cookie: Optional[Token] = Depends(get_auth_cookie),
    cookie: int = 1,
):
    if not cookie:
        raise UnauthorizedPageException()
    # retuen 204
    return Response(status_code=status.HTTP_200_OK)


# edit component
@router.get(
    path="/edit/{restaurant_id}",
    summary="Open the edit modal for a restaurant.",
    tags=["Restaurant"],
)
async def add_update_restaurant_modal_prompt(
    request: Request,
    restaurant_id: int,
    # cookie: Optional[Token] = Depends(get_auth_cookie),
    cookie: int = 1,
):
    if not cookie:
        raise UnauthorizedPageException()
    if restaurant_id == 0:
        restaurant = {
            "id": "",
            "name": "",
            "address": "",
            "phone": "",
            "email": "",
            "website": "",
            "image": "",
        }
        properties = {
            "title": "Add Restaurant",
            "description": "Add your restaurant to the list.",
        }
    else:
        restaurant = {
            "id": restaurant_id,
            "name": f"Restaurant{restaurant_id}",
            "address": "1234 Main St.",
            "phone": "123-456-7890",
            "email": "abc@abc.com",
            "website": "https://www.google.com",
            "image": "https://via.placeholder.com/150",
        }
        properties = {
            "title": "Edit Restaurant info",
            "description": "Edit your restaurant information.",
        }
    context = {"request": request, "restaurant": restaurant, "properties": properties}
    return templates.TemplateResponse(
        "partials/restaurant/restaurant_edit.html", context
    )
