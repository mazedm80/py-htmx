from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app import templates
from app.utils.auth import User, get_userinfo_for_page
from app.utils.exceptions import UnauthorizedPageException

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get(
    path="",
    summary="Gets the main dashboard page",
    tags=["Pages"],
    response_class=HTMLResponse,
)
async def get_dashboard(
    request: Request,
    user: Optional[User] = Depends(get_userinfo_for_page),
) -> HTMLResponse:
    title = "dashboard"
    if not user:
        raise UnauthorizedPageException()
    context = {
        "request": request,
        "title": title,
        "user": user,
        "nav_menu": "false",
    }
    return templates.TemplateResponse("pages/dashboard.html", context)
