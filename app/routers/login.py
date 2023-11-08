from typing import Optional, Dict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app import templates
from app.utils.auth import AuthoToken, Token, get_login_form_creds
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
    auth_token: AuthoToken = Depends(get_login_form_creds),  # get_login_form_creds
) -> dict:
    if auth_token:
        response = RedirectResponse("/dashboard", status_code=302)
        response.set_cookie(
            key=auth_token.token_name,
            value=auth_token.access_token,
            expires=auth_token.expires_in,
            httponly=True,
            secure=True,
        )
    else:
        response = RedirectResponse("/login?invalid=True", status_code=302)

    return response


@router.get(
    path="/register",
    summary="Gets the login page",
    tags=["Pages", "Authentication"],
    response_class=HTMLResponse,
)
async def get_login(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("pages/register.html", context)


logout = dict(path="/logout", summary="Logs out of the app", tags=["Authentication"])


@router.get(**logout)
@router.post(**logout)
async def post_login(cookie: Optional[Token] = Depends(get_login_form_creds)) -> dict:
    if not cookie:
        raise UnauthorizedPageException()

    response = RedirectResponse("/login?logged_out=True", status_code=302)
    response.set_cookie(key=cookie.name, value=cookie.token, expires=-1)
    return response
