from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app import templates
from app.services.menu import get_menu_categories, get_menu_items
from app.utils.auth import User, UserSession, get_user_session, get_userinfo_for_page

router = APIRouter(
    prefix="/order",
    tags=["order"],
)


# Order page routers
# Order page
@router.get(
    path="",
    summary="Gets the Order page.",
    tags=["Pages"],
    response_class=HTMLResponse,
)
async def get_order_page(
    request: Request,
    user: Optional[User] = Depends(get_userinfo_for_page),
) -> HTMLResponse:
    context = {
        "request": request,
        "title": "order",
        "user": user,
    }
    return templates.TemplateResponse("pages/order.html", context)


# Get menus by category page
@router.get(
    path="/menu/{category_id}",
    summary="Gets the POS menu page.",
    tags=["Pages"],
    response_class=HTMLResponse,
)
async def get_pos_menu_page(
    request: Request,
    category_id: int,
    session: Optional[UserSession] = Depends(get_user_session),
) -> HTMLResponse:
    menus = await get_menu_items(
        user_session=session.user_session, category_id=category_id
    )
    trimmed_menus = []
    for menu in menus:
        trimmed_menus.append(
            {
                "id": menu["id"],
                "name": menu["name"],
                "price": menu["price"],
                "description": menu["description"],
                "making_time": menu["making_time"],
                "spice_level": menu["spice_level"],
                "image": menu["image"],
            }
        )
    context = {
        "request": request,
        "menus": trimmed_menus * 5,
    }
    return templates.TemplateResponse("partials/pos/menus.html", context)
