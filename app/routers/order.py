from typing import Optional, Any, Dict, List

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from app import templates
from app.services.order import post_order
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


# create order
@router.post(
    path="",
    summary="Creates an order.",
    tags=["Order"],
    status_code=200,
)
async def create_order(
    request: Request,
    body: Dict[str, Any],
    user_session: UserSession = Depends(get_user_session),
) -> None:
    status_code = await post_order(data=body, user_session=user_session.user_session)
    return status_code
