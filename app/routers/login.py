from typing import Optional, Dict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app import templates
from app.utils.auth import Token, get_login_form_creds, get_auth_cookie, set_auth_cookie
from app.utils.exceptions import UnauthorizedPageException

router = APIRouter()


@router.get(
    path="/login",
    summary="Gets the login page",
    tags=["Pages", "Authentication"],
    response_class=HTMLResponse,
)
async def get_login(
    request: Request,
    invalid: Optional[bool] = None,
    logged_out: Optional[bool] = None,
    unauthorized: Optional[bool] = None,
):
    context = {
        "request": request,
        "invalid": invalid,
        "logged_out": logged_out,
        "unauthorized": unauthorized,
    }
    return templates.TemplateResponse("pages/login.html", context)


@router.post(path="/login", summary="Logs into the app", tags=["Authentication"])
async def post_login(
    cookie: Dict | Token = Depends(set_auth_cookie),  # get_login_form_creds
) -> dict:
    if cookie:
        print(cookie["remember_me"])
        response = RedirectResponse("/dashboard", status_code=302)
        response.set_cookie(key="remember", value=cookie["remember_me"])
        # response.set_cookie(key="test", value=cookie.access_token)
    else:
        response = RedirectResponse("/login?invalid=True", status_code=302)

    return response


logout = dict(path="/logout", summary="Logs out of the app", tags=["Authentication"])


@router.get(**logout)
@router.post(**logout)
async def post_login(cookie: Optional[Token] = Depends(get_auth_cookie)) -> dict:
    if not cookie:
        raise UnauthorizedPageException()

    response = RedirectResponse("/login?logged_out=True", status_code=302)
    response.set_cookie(key=cookie.name, value=cookie.token, expires=-1)
    return response
