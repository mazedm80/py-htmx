from typing import Optional

from fastapi import APIRouter, Request, Response, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

from app import templates
from app.services.menu import get_menu_categories, get_menu_items
from app.utils.auth import User, get_userinfo_for_page, UserSession, get_user_session
from app.utils.exceptions import UnauthorizedPageException

router = APIRouter(
    prefix="/pos",
    tags=["pos"],
)


# POS page routers
# POS page
@router.get(
    path="",
    summary="Gets the POS page.",
    tags=["Pages"],
    response_class=HTMLResponse,
)
async def get_pos_page(
    request: Request,
    user: Optional[User] = Depends(get_userinfo_for_page),
    session: Optional[UserSession] = Depends(get_user_session),
) -> HTMLResponse:
    categories = await get_menu_categories(user_session=session.user_session)
    context = {
        "request": request,
        "title": "pos",
        "user": user,
        "categories": categories * 2,
    }
    return templates.TemplateResponse("pages/pos.html", context)


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
                "image": menu["image"],
            }
        )
    context = {
        "request": request,
        "menus": trimmed_menus * 5,
    }
    return templates.TemplateResponse("partials/pos/menus.html", context)
