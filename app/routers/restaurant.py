from typing import Optional

import httpx
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app import templates
from app.utils.auth import Token, get_auth_cookie
from app.utils.exceptions import UnauthorizedPageException
from config.settings import settings

router = APIRouter(
    prefix="/restaurant",
    tags=["restaurant"],
)


@router.get(
    path="/",
    summary="Gets the restaurant page.",
    tags=["Pages"],
    response_class=HTMLResponse,
)
async def get_dashboard(
    request: Request,
    # cookie: Optional[Token] = Depends(get_auth_cookie),
    cookie: int = 1,
):
    restaurant = {
        "name": "Restaurant",
        "description": "This is a restaurant.",
        "address": "1234 Main St.",
        "city": "City",
        "state": "ST",
        "zip": "12345",
        "phone": "123-456-7890",
        "email": "abc@abc.com",
    }
    context = {"request": request}
    if not cookie:
        raise UnauthorizedPageException()
    return templates.TemplateResponse("pages/restaurant.html", context)
