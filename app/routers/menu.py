from typing import Optional

import httpx
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse

from app import templates
from app.services.menu import (
    get_menu_form_creds,
    get_menu_item,
    add_menu_item,
    update_menu_item,
    delete_menu_item,
)
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


# View menu item page
@router.get(
    path="/view/{menu_id}",
    summary="Gets the menu item view page.",
    tags=["Pages"],
    response_class=RedirectResponse,
)
async def get_view_menu_page(
    menu_id: int,
    request: Request,
    session: Optional[UserSession] = Depends(get_user_session),
) -> HTMLResponse:
    item = await get_menu_item(menu_id=menu_id, user_session=session.user_session)
    title = "View Menu"
    context = {"request": request, "item": item, "title": title, "nav_menu": "true"}
    return templates.TemplateResponse("pages/menu_view.html", context)


# Edit menu item page
@router.get(
    path="/edit/{menu_id}",
    summary="Gets the menu item edit page.",
    tags=["Pages"],
    response_class=RedirectResponse,
)
async def get_edit_menu_page(
    menu_id: int,
    request: Request,
    session: Optional[UserSession] = Depends(get_user_session),
) -> HTMLResponse:
    item = await get_menu_item(menu_id=menu_id, user_session=session.user_session)
    title = "Edit Menu"
    context = {"request": request, "item": item, "title": title, "nav_menu": "true"}
    return templates.TemplateResponse("pages/menu_edit.html", context)


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


# Add menu item
@router.post(
    path="/data/add",
    summary="Adds the menu item.",
    tags=["Pages"],
    response_class=RedirectResponse,
)
async def add_menu_data(
    data: dict = Depends(get_menu_form_creds),
    session: Optional[UserSession] = Depends(get_user_session),
) -> RedirectResponse:
    status_code = await add_menu_item(data=data, user_session=session.user_session)
    if status_code == 200:
        return RedirectResponse(url="/menu", status_code=303)


# Edit menu item
@router.post(
    path="/data/edit/{menu_id}",
    summary="Edits the menu item.",
    tags=["Pages"],
    response_class=RedirectResponse,
)
async def edit_menu_data(
    menu_id: int,
    data: dict = Depends(get_menu_form_creds),
    session: Optional[UserSession] = Depends(get_user_session),
) -> RedirectResponse:
    status_code = await update_menu_item(
        data=data, menu_id=menu_id, user_session=session.user_session
    )
    if status_code == 200:
        return RedirectResponse(url="/menu", status_code=303)


# Delete menu item
@router.delete(
    path="/{menu_id}",
    summary="Deletes the menu item.",
    tags=["Pages"],
)
async def delete_menu_data(
    menu_id: int,
    session: Optional[UserSession] = Depends(get_user_session),
) -> None:
    status_code = await delete_menu_item(
        menu_id=menu_id, user_session=session.user_session
    )
    return Response(status_code=status_code)


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
