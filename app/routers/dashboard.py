from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app import templates
from app.utils.auth import AuthCookie, get_auth_cookie, get_login_form_creds
from app.utils.exceptions import UnauthorizedPageException

router = APIRouter()


@router.get(
    path="/dashboard",
    summary="Gets the main dashboard page",
    tags=["Pages"],
    response_class=HTMLResponse,
)
async def get_dashboard(
    request: Request,
    cookie: Optional[AuthCookie] = Depends(get_auth_cookie),
):
    context = {"request": request}
    if not cookie:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("pages/dashboard.html", context)