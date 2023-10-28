from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from app import templates
from app.utils.auth import Token, get_auth_cookie

router = APIRouter()


@router.get(
    path="/", summary="Redirects to the login or dashboard pages", tags=["Pages"]
)
async def read_root(cookie: Optional[Token] = Depends(get_auth_cookie)):
    path = "/dashboard" if cookie else "/login"
    return RedirectResponse(path, status_code=302)


# @router.get(path="/favicon.ico", include_in_schema=False)
# async def get_favicon():
#     return FileResponse("static/img/favicon.ico")


@router.get(path="/not-found", summary='Gets the "Not Found" page', tags=["Pages"])
async def get_not_found(request: Request):
    return templates.TemplateResponse("pages/not-found.html", {"request": request})
