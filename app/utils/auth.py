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


class User(BaseModel):
    """User schema."""

    id: int
    name: str
    email: str
    auth_group: int


def create_cookie(
    token: Token,
    remember_me: bool = False,
) -> AuthoToken:
    """Creates a cookie."""

    expires_in = 60 * 60 * 24 * 7 if remember_me else 60 * 60 * 24

    return AuthoToken(
        token_name="user_session",
        access_token=token.access_token,
        expires_in=expires_in,
    )


def get_login_form_creds(
    email: str = Form(), password: str = Form(), remember_me: bool = Form(default=False)
) -> Optional[AuthoToken]:
    cookie = None
    with httpx.Client() as client:
        response = client.post(
            f"{settings.api_host}/auth/login",
            params={"email": email, "password": password},
        )
        if response.status_code == 200:
            token = response.json()
            cookie = Token.model_validate(token)
            cookie = create_cookie(cookie, remember_me=remember_me)
    return cookie


def register_user(
    name: str = Form(),
    bday: str = Form(),
    email: str = Form(),
    password: str = Form(),
    password2: str = Form(),
    role: str = Form(),
):
    if password != password2:
        raise UnauthorizedException()
    with httpx.Client() as client:
        response = client.post(
            f"{settings.api_host}/auth/register",
            params={
                "name": name,
                "bday": bday,
                "email": email,
                "password": password,
                "role": role,
            },
        )
        if response.status_code == 200:
            token = response.json()
            cookie = Token.model_validate(token)
            cookie = create_cookie(cookie)
    return cookie


def get_userinfo_for_page(user_session: Optional[str] = Cookie(default=None)) -> User:
    if not user_session:
        raise UnauthorizedPageException()
    with httpx.Client() as client:
        response = client.get(
            f"{settings.api_host}/auth/me",
            headers={"Authorization": f"Bearer {user_session}"},
        )
        if response.status_code == 200:
            user = response.json()
            return User.model_validate(user)
        else:
            raise UnauthorizedPageException()
