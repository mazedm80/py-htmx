from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.routers import dashboard, login, menu, restaurant, root, pos
from app.utils.exceptions import NotFoundException, UnauthorizedPageException

app = FastAPI(
    docs_url=None,  # Disable docs (Swagger UI)
    redoc_url=None,  # Disable redoc
)
app.include_router(root.router)
app.include_router(login.router)
app.include_router(dashboard.router)
app.include_router(restaurant.router)
app.include_router(menu.router)
app.include_router(pos.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

# --------------------------------------------------------------------------------
# Exception Handlers
# --------------------------------------------------------------------------------


@app.exception_handler(UnauthorizedPageException)
async def unauthorized_exception_handler(
    request: Request, exc: UnauthorizedPageException
):
    return RedirectResponse("/login?unauthorized=True", status_code=302)


@app.exception_handler(404)
async def page_not_found_exception_handler(request: Request, exc: NotFoundException):
    return RedirectResponse("/not-found", status_code=302)
