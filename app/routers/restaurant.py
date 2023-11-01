from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app import templates
from app.utils.auth import Token, get_auth_cookie
from app.utils.exceptions import UnauthorizedPageException

router = APIRouter()


@router.get(
    path="/restaurant",
    summary="Gets the restaurant page",
    tags=["Pages"],
    response_class=HTMLResponse,
)
async def get_dashboard(
    request: Request,
    # cookie: Optional[Token] = Depends(get_auth_cookie),
    cookie: int = 1,
):
    context = {"request": request}
    if not cookie:
        raise UnauthorizedPageException()
    return templates.TemplateResponse("pages/restaurant.html", context)
