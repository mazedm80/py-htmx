import secrets
from typing import Optional

import httpx
from fastapi import Cookie, Depends, Form, Request
from pydantic import BaseModel, field_validator

from app.utils.exceptions import UnauthorizedException, UnauthorizedPageException
from config.settings import settings


class Token(BaseModel):
    """Token schema."""

    access_token: str
    token_type: str

    @field_validator("token_type")
    @classmethod
    def validate_token_type(cls, token_type: str):
        if token_type != "bearer":
            raise ValueError("Invalid token type")
        return token_type


class AuthoToken(BaseModel):
    """Autho token schema."""

    token_name: str
    access_token: str
    expires_in: int
    id_token: str
    scope: str
    token_type: str
    refresh_token: str
    user_id: str


def get_login_form_creds(
    email: str = Form(), password: str = Form(), remember_me: bool = Form(default=False)
) -> Optional[Token]:
    cookie = None
    # with httpx.Client() as client:
    #     response = client.post(
    #         f"{settings.api_host}/auth/login",
    #         params={"email": email, "password": password},
    #     )
    #     if response.status_code == 200:
    #         token = response.json()
    #         cookie = Token.model_validate(token)
    return cookie


def set_auth_cookie(
    email: str = Form(), password: str = Form(), remember_me: bool = Form(default=False)
):
    return {
        "email": email,
        "password": password,
        "remember_me": remember_me,
    }


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
