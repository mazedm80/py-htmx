from typing import Optional

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app import templates
from app.utils.exceptions import UnauthorizedPageException

router = APIRouter(
    prefix="/menu",
    tags=["menu"],
)


# Menu page
@router.get(
    path="",
    summary="Gets the menu page.",
    tags=["Pages"],
    response_class=HTMLResponse,
)
async def get_menu_page(
    request: Request,
    # cookie: Optional[Token] = Depends(get_auth_cookie),
    cookie: int = 1,
    initial_id: Optional[int] = None,
):
    menu_list = []
    for i in range(1, 10):
        menu_list.append(
            {
                "id": i,
                "restaurant_id": i + 10,
                "menu_category": "Burgers",
                "name": f"Menu{i}",
                "description": "This is a description.",
                "price": 10 + i,
                "status": False,
                "image": "https://pngfre.com/wp-content/uploads/Burger-45-300x278.png",
                "vegetarian": True,
                "vegan": False,
                "gluten_free": True,
                "spicy": False,
            }
        )
    title = "Menu List"
    context = {
        "request": request,
        "menu_list": menu_list,
        "initial_id": 1,
        "title": title,
        "nav_menu": "true",
    }
    if not cookie:
        raise UnauthorizedPageException()
    return templates.TemplateResponse("pages/menu.html", context)


# Add menu page
@router.get(
    path="/add",
    summary="Gets the add menu page.",
    tags=["Pages"],
    response_class=HTMLResponse,
)
async def get_add_menu_page(
    request: Request,
    # cookie: Optional[Token] = Depends(get_auth_cookie),
    cookie: int = 1,
    initial_id: Optional[int] = None,
):
    title = "Add Menu"
    context = {
        "request": request,
        "initial_id": 1,
        "title": title,
        "nav_menu": "true",
    }
    if not cookie:
        raise UnauthorizedPageException()
    return templates.TemplateResponse("pages/menu_add.html", context)


# Get item category list dropdown
@router.get(
    path="/category/dropdown",
    summary="Gets the item category list page.",
    tags=["Pages"],
    response_class=HTMLResponse,
)
async def get_options_page(
    request: Request,
    cookie: int = 1,
):
    options = []
    for i in range(1, 10):
        options.append(f"Category{i}")
    name = "Product Category List"
    context = {
        "request": request,
        "options": options,
        "id": "menu_category",
        "name": name,
    }
    if not cookie:
        raise UnauthorizedPageException()
    return templates.TemplateResponse("components/form/dropdown.html", context)
