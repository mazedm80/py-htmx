from typing import Optional, Any, Dict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app import templates
from app.services.order import post_order, get_order_by_status, get_order_details_by_id
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


# Order prepared list component
@router.get(
    path="/list/pending",
    summary="Gets the Pending Order list component.",
    tags=["Components"],
    response_class=HTMLResponse,
)
async def get_pending_order_list_component(
    request: Request,
    session: Optional[UserSession] = Depends(get_user_session),
) -> HTMLResponse:
    orders = await get_order_by_status(
        status="pending", user_session=session.user_session
    )
    context = {"request": request, "orders": orders}
    return templates.TemplateResponse("partials/order/order_list.html", context)


# Order accepted list component
@router.get(
    path="/list/accepted",
    summary="Gets the Accepted Order list component.",
    tags=["Components"],
    response_class=HTMLResponse,
)
async def get_accepted_order_list_component(
    request: Request,
    user: Optional[User] = Depends(get_userinfo_for_page),
) -> HTMLResponse:
    context = {"request": request}
    return templates.TemplateResponse(
        "partials/order/order_list_prepared.html", context
    )


# Order prepared list component
@router.get(
    path="/list/prepared",
    summary="Gets the Prepared Order list component.",
    tags=["Components"],
    response_class=HTMLResponse,
)
async def get_prepared_order_list_component(
    request: Request,
    user: Optional[User] = Depends(get_userinfo_for_page),
) -> HTMLResponse:
    context = {"request": request}
    return templates.TemplateResponse(
        "partials/order/order_list_prepared.html", context
    )


# Order completed list component
@router.get(
    path="/list/completed",
    summary="Gets the Order of completed and unpaid list component.",
    tags=["Components"],
    response_class=HTMLResponse,
)
async def get_completed_order_list_component(
    request: Request,
    user: Optional[User] = Depends(get_userinfo_for_page),
) -> HTMLResponse:
    context = {"request": request}
    return templates.TemplateResponse(
        "partials/order/order_list_delivered.html", context
    )


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
