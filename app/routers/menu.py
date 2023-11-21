from typing import Optional

import httpx
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse

from app import templates
from app.services.menu import (
    get_menu_form_creds,
    get_menu_category_form_creds,
    get_menu_categories,
    get_menu_category,
    add_menu_category,
    update_menu_category,
    delete_menu_category,
    get_menu_item,
    get_menu_items,
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
    session: Optional[UserSession] = Depends(get_user_session),
):
    menu_list = await get_menu_items(user_session=session.user_session)
    title = "Menu"
    context = {
        "request": request,
        "title": title,
        "user": user,
        "menu_list": menu_list,
    }
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
    user: Optional[User] = Depends(get_userinfo_for_page),
) -> HTMLResponse:
    title = "Add Menu"
    context = {"request": request, "title": title, "user": user}
    return templates.TemplateResponse("pages/menu_add.html", context)


# View menu item page
@router.get(
    path="/view/{menu_id}",
    summary="Gets the menu item view page.",
    tags=["Pages"],
    response_class=HTMLResponse,
)
async def get_view_menu_page(
    menu_id: int,
    request: Request,
    user: Optional[User] = Depends(get_userinfo_for_page),
    session: Optional[UserSession] = Depends(get_user_session),
) -> HTMLResponse:
    item = await get_menu_item(menu_id=menu_id, user_session=session.user_session)
    title = "View Menu"
    context = {"request": request, "item": item, "title": title, "user": user}
    return templates.TemplateResponse("pages/menu_view.html", context)


# Edit menu item page
@router.get(
    path="/edit/{menu_id}",
    summary="Gets the menu item edit page.",
    tags=["Pages"],
    response_class=HTMLResponse,
)
async def get_edit_menu_page(
    menu_id: int,
    request: Request,
    user: Optional[User] = Depends(get_userinfo_for_page),
    session: Optional[UserSession] = Depends(get_user_session),
) -> HTMLResponse:
    item = await get_menu_item(menu_id=menu_id, user_session=session.user_session)
    title = "Edit Menu"
    context = {
        "request": request,
        "item": item,
        "title": title,
        "user": user,
    }
    return templates.TemplateResponse("pages/menu_edit.html", context)


# Category list page
@router.get(
    path="/category",
    summary="Gets the item category list page.",
    tags=["Pages"],
    response_class=HTMLResponse,
)
async def get_category_list_page(
    request: Request,
    user: Optional[User] = Depends(get_userinfo_for_page),
    session: Optional[UserSession] = Depends(get_user_session),
) -> HTMLResponse:
    name = "Category List"
    title = "Category"
    categories = await get_menu_categories(user_session=session.user_session)
    context = {
        "request": request,
        "name": name,
        "user": user,
        "title": title,
        "categories": categories,
    }
    return templates.TemplateResponse("pages/menu_category.html", context)


# Get item category add modal page
@router.get(
    path="/category/add",
    summary="Gets the item category add modal.",
    tags=["Pages"],
    response_class=HTMLResponse,
)
async def get_add_category_page(
    request: Request,
):
    title = "category"
    info = "Add a new category"
    context = {"request": request, "title": title, "info": info}
    return templates.TemplateResponse("partials/menu/category_add.html", context)


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
    summary="Gets the item category list dropdown.",
    tags=["Pages"],
    response_class=HTMLResponse,
)
async def get_options_page(
    request: Request,
    session: Optional[UserSession] = Depends(get_user_session),
):
    options = await get_menu_categories(user_session=session.user_session)
    name = "Category"
    context = {"request": request, "name": name, "options": options}
    return templates.TemplateResponse("partials/menu/category_list.html", context)


# Post item category
@router.post(
    path="/category",
    summary="Adds the item category.",
    tags=["Pages"],
    response_class=RedirectResponse,
)
async def add_category_data(
    data: dict = Depends(get_menu_category_form_creds),
    session: Optional[UserSession] = Depends(get_user_session),
) -> RedirectResponse:
    status_code = await add_menu_category(data=data, user_session=session.user_session)
    if status_code == 200:
        return RedirectResponse(url="/menu/category", status_code=303)
