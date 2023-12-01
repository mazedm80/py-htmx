from typing import Optional, Any, Dict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app import templates
from app.services.order import (
    post_order,
    get_order_by_status,
    get_order_details_by_id,
    update_order_status,
)
from app.utils.auth import (
    User,
    UserSession,
    get_user_session,
    get_userinfo_for_page,
    UnauthorizedPageException,
)

router = APIRouter(
    prefix="/order",
    tags=["order"],
)


# Order page routers
# Order page
@router.get(
    path="/sales",
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


# Order kitchen view page
@router.get(
    path="/kitchen",
    summary="Gets the Order kitchen view page.",
    tags=["Pages"],
    response_class=HTMLResponse,
)
async def get_order_kitchen_view_page(
    request: Request,
    user: Optional[User] = Depends(get_userinfo_for_page),
    session: Optional[UserSession] = Depends(get_user_session),
) -> HTMLResponse:
    orders = await get_order_by_status(
        payment_status=None,
        user_session=session.user_session,
        status="accepted",
    )
    context = {
        "request": request,
        "title": "kitchen",
        "user": user,
        "orders": orders,
    }
    return templates.TemplateResponse("pages/kitchen.html", context)


# Order list by status component
@router.get(
    path="/list/status",
    summary="Gets the Order list by ststus component.",
    tags=["Components"],
    response_class=HTMLResponse,
)
async def get_pending_order_list_component(
    request: Request,
    status: Optional[str] = None,
    payment_status: Optional[str] = None,
    session: Optional[UserSession] = Depends(get_user_session),
) -> HTMLResponse:
    if status and payment_status is None:
        orders = await get_order_by_status(
            status=status, user_session=session.user_session, payment_status=None
        )
    elif payment_status and status is None:
        orders = await get_order_by_status(
            payment_status=payment_status,
            user_session=session.user_session,
            status=None,
        )

    context = {"request": request, "orders": orders}
    return templates.TemplateResponse("partials/order/order_list.html", context)


# Order details component
@router.get(
    path="/details/{order_id}",
    summary="Gets the Order details component.",
    tags=["Components"],
    response_class=HTMLResponse,
)
async def get_order_details_component(
    order_id: str,
    request: Request,
    session: Optional[UserSession] = Depends(get_user_session),
) -> HTMLResponse:
    order, order_details = await get_order_details_by_id(
        order_id=order_id, user_session=session.user_session
    )
    context = {
        "request": request,
        "order_id": order_id,
        "order": order,
        "order_details": order_details,
    }
    return templates.TemplateResponse("partials/order/order_details.html", context)


# Order data routers
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


# update order status to accepted
@router.put(
    path="/{status}/{order_id}",
    summary="Updates an order.",
    tags=["Order"],
    response_class=HTMLResponse,
)
async def update_order_status_to_accepted(
    status: str,
    order_id: str,
    request: Request,
    user_session: UserSession = Depends(get_user_session),
) -> HTMLResponse:
    if status == "accepted":
        status_code = await update_order_status(
            status=status,
            order_id=order_id,
            user_session=user_session.user_session,
            payment_status=None,
        )
    elif status == "prepared":
        status_code = await update_order_status(
            status=status,
            payment_status=None,
            order_id=order_id,
            user_session=user_session.user_session,
        )
    elif status == "cancelled":
        status_code = await update_order_status(
            status=None,
            payment_status=status,
            order_id=order_id,
            user_session=user_session.user_session,
        )
    elif status == "completed":
        status_code = await update_order_status(
            status=status,
            payment_status=None,
            order_id=order_id,
            user_session=user_session.user_session,
        )
    if status_code != 200:
        raise UnauthorizedPageException
    orders = await get_order_by_status(
        status="pending", user_session=user_session.user_session, payment_status=None
    )
    context = {"request": request, "orders": orders}
    return templates.TemplateResponse("partials/order/order_list.html", context)
