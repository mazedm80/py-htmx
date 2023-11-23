from typing import Optional

from fastapi import APIRouter, Request, Response, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

from app import templates
from app.services.restaurant import (
    get_restaurant_form_creds,
    add_restaurant,
    update_restaurant,
    get_restaurant,
    get_restaurants,
    delete_restaurant,
)
from app.utils.auth import User, get_userinfo_for_page, UserSession, get_user_session
from app.utils.exceptions import UnauthorizedPageException

router = APIRouter(
    prefix="/restaurant",
    tags=["restaurant"],
)


# Restaurant page routers
# Restaurant page
@router.get(
    path="",
    summary="Gets the restaurant page.",
    tags=["Pages"],
    response_class=HTMLResponse,
)
async def get_dashboard(
    request: Request,
    user: Optional[User] = Depends(get_userinfo_for_page),
    session: Optional[UserSession] = Depends(get_user_session),
):
    restaurants = await get_restaurants(user_session=session.user_session)
    title = "restaurant"
    context = {
        "request": request,
        "title": title,
        "user": user,
        "restaurants": restaurants,
    }
    if not user:
        raise UnauthorizedPageException()
    return templates.TemplateResponse("pages/restaurant.html", context)


# Add/Edit restaurant modal
@router.get(
    path="/add",
    summary="Open the add modal for a restaurant.",
    tags=["Restaurant"],
)
async def add_edit_restaurant_info(
    request: Request,
    restaurant_id: Optional[int] = None,
    session: Optional[UserSession] = Depends(get_user_session),
) -> HTMLResponse:
    title = "Restaurant"
    if restaurant_id:
        restaurant = await get_restaurant(
            restaurant_id=restaurant_id, user_session=session.user_session
        )
        info = "Edit restaurant informaton"
        context = {
            "request": request,
            "title": title,
            "info": info,
            "restaurant": restaurant,
        }
    else:
        info = "Add a new restaurant"
        context = {"request": request, "title": title, "info": info, "restaurant": None}
    return templates.TemplateResponse(
        "partials/restaurant/restaurant_edit.html", context
    )


# Restaurant data routers
# Get Restaurant
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
    restaurants = await get_restaurants(user_session=session.user_session)
    context = {"request": request, "menu_list": []}
    return templates.TemplateResponse("partials/menu/menu_list.html", context)


# Edit Restaurant
@router.post(
    path="/data/edit/{restaurant_id}",
    summary="Updates the menu item.",
    tags=["Pages"],
    response_class=RedirectResponse,
)
async def edit_restaurant_data(
    restaurant_id: int,
    data: dict = Depends(get_restaurant_form_creds),
    session: Optional[UserSession] = Depends(get_user_session),
) -> RedirectResponse:
    status_code = await update_restaurant(
        data=data, restaurant_id=restaurant_id, user_session=session.user_session
    )
    if status_code == 200:
        return RedirectResponse(url="/restaurant", status_code=303)


# Add restaurant
@router.post(
    path="/data/add",
    summary="Adds the menu item.",
    tags=["Pages"],
    response_class=RedirectResponse,
)
async def add_menu_data(
    data: dict = Depends(get_restaurant_form_creds),
    session: Optional[UserSession] = Depends(get_user_session),
) -> RedirectResponse:
    print(data)
    status_code = await add_restaurant(data=data, user_session=session.user_session)
    if status_code == 200:
        return RedirectResponse(url="/restaurant", status_code=303)


@router.delete(
    path="/{restaurant_id}",
    summary="Deletes a restaurant.",
    tags=["Restaurant"],
)
async def delete_restaurant_data(
    restaurant_id: int,
    session: Optional[UserSession] = Depends(get_user_session),
) -> None:
    status_code = await delete_restaurant(
        restaurant_id=restaurant_id, user_session=session.user_session
    )
    return Response(status_code=status_code)


# view component
@router.get(
    path="/view/{tab}/{restaurant_id}",
    summary="Open the edit modal for a restaurant.",
    tags=["Restaurant"],
)
async def view_restaurant_info(
    request: Request,
    restaurant_id: int,
    tab: str,
    # cookie: Optional[Token] = Depends(get_auth_cookie),
    cookie: int = 1,
):
    if not cookie:
        raise UnauthorizedPageException()
    if tab == "general" or tab == "complete":
        data = {
            "id": restaurant_id,
            "name": f"Restaurant{restaurant_id}",
            "address": "1234 Main St.",
            "phone": "123-456-7890",
            "email": f"abc_{restaurant_id}@gmail.com",
            "website": "https://www.google.com",
            "image": "https://showme.co.za/hartbeespoort/files/2021/10/MCDONALDS_BANNER.png",
        }
    elif tab == "account":
        data = {
            "tax_rate": 15.0,
            "tax_included": True,
            "monthly_target": 10000.0,
        }
    context = {"request": request, "data": data}
    return templates.TemplateResponse(f"partials/restaurant/view_{tab}.html", context)


# edit component
@router.get(
    path="/edit/{tab}/{restaurant_id}",
    summary="Open the edit modal for a restaurant.",
    tags=["Restaurant"],
)
async def edit_restaurant_info(
    request: Request,
    restaurant_id: int,
    tab: str,
    # cookie: Optional[Token] = Depends(get_auth_cookie),
    cookie: int = 1,
):
    if not cookie:
        raise UnauthorizedPageException()
    if tab == "general":
        data = {
            "id": restaurant_id,
            "name": f"Restaurant{restaurant_id}",
            "address": "1234 Main St.",
            "phone": "123-456-7890",
            "email": f"abc_{restaurant_id}@gmail.com",
            "website": "https://www.google.com",
            "image": "https://via.placeholder.com/150",
        }
    elif tab == "account":
        data = {
            "tax_rate": 15.0,
            "tax_included": True,
            "monthly_target": 10000.0,
        }
    context = {"request": request, "data": data}
    return templates.TemplateResponse(f"partials/restaurant/edit_{tab}.html", context)


# add component
@router.get(
    path="/add",
    summary="Open the add modal for a restaurant.",
    tags=["Restaurant"],
)
async def add_restaurant_info(
    request: Request,
    # cookie: Optional[Token] = Depends(get_auth_cookie),
    cookie: int = 1,
):
    if not cookie:
        raise UnauthorizedPageException()
    title = "restaurant"
    info = "Add a new restaurant"
    context = {"request": request, "title": title, "info": info}
    return templates.TemplateResponse(
        "partials/restaurant/restaurant_edit.html", context
    )


#  Mics
# Get image upload section
@router.get(
    path="/image",
    summary="Gets the photo upload section.",
    tags=["Pages"],
    response_class=HTMLResponse,
)
async def get_image_upload_page(
    request: Request,
) -> HTMLResponse:
    context = {"request": request}
    return templates.TemplateResponse("components/form/upload_image.html", context)
