import secrets
from typing import Optional

import httpx
from fastapi import Cookie, Depends, Form
from pydantic import BaseModel

from app import secret_key, users
from app.utils.exceptions import UnauthorizedException, UnauthorizedPageException
from config.settings import settings


class Token(BaseModel):
    """Token schema."""

    access_token: str
    token_type: str


def get_login_form_creds(
    email: str = Form(), password: str = Form()
) -> Optional[Token]:
    cookie = None
    username = email
    print(f"username = {username} and password = {password}")
    with httpx.Client() as client:
        response = client.post(
            f"{settings.api_host}/auth/login",
            data={"username": username, "password": password},
        )
        if response.status_code == 200:
            token = response.json()
            print(f"token = {token}")
            cookie = Token(
                access_token=token["access_token"], token_type=token["token_type"]
            )

    return cookie


def get_auth_cookie(
    reminders_session: Optional[str] = Cookie(default=None),
) -> Optional[Token]:
    cookie = None
    print(f"reminders_session = {reminders_session}")
    if reminders_session:
        with httpx.Client() as client:
            response = client.get(
                f"{settings.api_host}/auth/login",
                headers={"Authorization": f"Bearer {reminders_session}"},
            )
            if response.status_code == 200:
                token = response.json()
                cookie = Token(
                    access_token=token["access_token"], token_type=token["token_type"]
                )
    return cookie


def get_username_for_api(
    cookie: Optional[Token] = Depends(get_auth_cookie),
) -> str:
    if not cookie:
        raise UnauthorizedException()

    return cookie.username


def get_username_for_page(
    cookie: Optional[Token] = Depends(get_auth_cookie),
) -> str:
    if not cookie:
        raise UnauthorizedPageException()

    return cookie.username
