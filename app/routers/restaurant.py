from typing import Optional

from fastapi import APIRouter, Request, Response, status
from fastapi.responses import HTMLResponse

from app import templates
from app.utils.exceptions import UnauthorizedPageException

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
    initial_id: Optional[int] = None,
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
                "image": "https://showme.co.za/hartbeespoort/files/2021/10/MCDONALDS_BANNER.png",
            }
        )
    title = "Restaurant"
    context = {
        "request": request,
        "restaurant_list": restaurant_list,
        "initial_id": 1,
        "title": title,
        "nav_menu": "false",
    }
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
