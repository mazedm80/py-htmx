import secrets
from typing import Optional

from fastapi import Cookie, Depends, Form
from fastapi.security import HTTPBasic
from jose import jwt
from pydantic import BaseModel

from app import secret_key, users
from app.utils.exceptions import UnauthorizedException, UnauthorizedPageException

basic_auth = HTTPBasic(auto_error=False)
auth_cookie_name = "reminders_session"


class AuthCookie(BaseModel):
    name: str
    token: str
    username: str


def serialize_token(username: str) -> str:
    return jwt.encode({"username": username}, secret_key, algorithm="HS256")


def deserialize_token(token: str) -> str:
    try:
        data = jwt.decode(token, secret_key, algorithms=["HS256"])
        return data["username"]
    except Exception:
        return None


def get_login_form_creds(
    username: str = Form(), password: str = Form()
) -> Optional[AuthCookie]:
    cookie = None

    if username in users:
        if secrets.compare_digest(password, users[username]):
            token = serialize_token(username)
            cookie = AuthCookie(name=auth_cookie_name, username=username, token=token)

    return cookie


def get_auth_cookie(
    reminders_session: Optional[str] = Cookie(default=None),
) -> Optional[AuthCookie]:
    cookie = None
    print(f"reminders_session = {reminders_session}")
    if reminders_session:
        username = deserialize_token(reminders_session)
        if username and username in users:
            cookie = AuthCookie(
                name=auth_cookie_name, username=username, token=reminders_session
            )

    return cookie


def get_username_for_api(
    cookie: Optional[AuthCookie] = Depends(get_auth_cookie),
) -> str:
    if not cookie:
        raise UnauthorizedException()

    return cookie.username


def get_username_for_page(
    cookie: Optional[AuthCookie] = Depends(get_auth_cookie),
) -> str:
    if not cookie:
        raise UnauthorizedPageException()

    return cookie.username
