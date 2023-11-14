
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app import templates
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
    # user: Optional[User] = Depends(get_userinfo_for_page),
    user: int = 1,
) -> HTMLResponse:
    title = "Dashboard"
    context = {"request": request, "title": title}
    if not user:
        raise UnauthorizedPageException()
    print(user)
    return templates.TemplateResponse("pages/dashboard.html", context)
