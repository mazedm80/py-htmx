import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseSettings
from starlette.exceptions import HTTPException

from app.routers import login, dashboard, root
from app.utils.exceptions import UnauthorizedPageException


class ApiSettings(BaseSettings):
    """Schema for configuring API parameters."""

    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    workers: int = 1

    class Config:
        env_prefix = "API_"
        env_file = ".env"
        env_file_encoding = "utf-8"


app = FastAPI(
    docs_url=None,  # Disable docs (Swagger UI)
    redoc_url=None,  # Disable redoc
)
app.include_router(root.router)
app.include_router(dashboard.router)
app.include_router(login.router)


# --------------------------------------------------------------------------------
# Static Files
# --------------------------------------------------------------------------------

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
async def page_not_found_exception_handler(request: Request, exc: HTTPException):
    if request.url.path.startswith("/api/"):
        return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)
    else:
        return RedirectResponse("/not-found")


if __name__ == "__main__":
    settings = ApiSettings()
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        workers=settings.workers,
        reload=settings.debug,
    )
