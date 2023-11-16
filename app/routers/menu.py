from typing import Optional

import httpx
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app import templates
from app.services.menu import get_menu_form_creds
from app.utils.auth import User, UserSession, get_user_session, get_userinfo_for_page
from app.utils.exceptions import UnauthorizedPageException
from config.settings import settings

router = APIRouter(
    prefix="/menu",
    tags=["menu"],
)


# Menu page routers
# Menu page
@router.get(
    path="",
    summary="Gets the menu page.",
    tags=["Pages"],
    response_class=HTMLResponse,
)
async def get_menu_page(
    request: Request,
    user: Optional[User] = Depends(get_userinfo_for_page),
):
    if not user:
        raise UnauthorizedPageException()
    title = "menu"
    context = {"request": request, "title": title, "nav_menu": "true"}
    return templates.TemplateResponse("pages/menu.html", context)


# Add menu page
@router.get(
    path="/add",
    summary="Gets the add menu page.",
    tags=["Pages"],
    response_class=HTMLResponse,
)
async def get_add_menu_page(
    request: Request,
    # cookie: Optional[Token] = Depends(get_auth_cookie),
    cookie: int = 1,
) -> HTMLResponse:
    title = "Add Menu"
    context = {
        "request": request,
        "initial_id": 1,
        "title": title,
        "nav_menu": "true",
    }
    if not cookie:
        raise UnauthorizedPageException()
    return templates.TemplateResponse("pages/menu_add.html", context)


# Menu data router
# Get menu data
@router.get(
    path="/data",
    summary="Gets the menu data.",
    tags=["Pages"],
    response_class=HTMLResponse,
)
async def get_menu_data(
    request: Request,
    session: Optional[UserSession] = Depends(get_user_session),
) -> HTMLResponse:
    with httpx.Client() as client:
        try:
            response = client.get(
                f"{settings.api_host}/menu",
                headers={"Authorization": f"Bearer {session.user_session}"},
            )
            response.raise_for_status()
            menu_list = response.json()["menu_items"]
        except httpx.HTTPError as e:
            print(e)
            menu_list = []
    context = {"request": request, "menu_list": menu_list}
    return templates.TemplateResponse("partials/menu/menu_list.html", context)


# Add menu data
@router.post(
    path="/data",
    summary="Adds the menu data.",
    tags=["Pages"],
    response_class=HTMLResponse,
)
async def add_menu_data(
    status_code: int = Depends(get_menu_form_creds),
) -> HTMLResponse:
    # if status_code != 201:
    #     raise UnauthorizedPageException()
    return RedirectResponse(url="/menu", status_code=303)


# Get item category list dropdown
@router.get(
    path="/category/dropdown",
    summary="Gets the item category list page.",
    tags=["Pages"],
    response_class=HTMLResponse,
)
async def get_options_page(
    request: Request,
    cookie: int = 1,
):
    options = []
    for i in range(1, 10):
        options.append(f"Category{i}")
    name = "Product Category List"
    context = {
        "request": request,
        "options": options,
        "id": "menu_category",
        "name": name,
    }
    if not cookie:
        raise UnauthorizedPageException()
    return templates.TemplateResponse("components/form/dropdown.html", context)
