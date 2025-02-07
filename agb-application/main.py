from contextlib import asynccontextmanager
from core.models import db_helper
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from api import router as api_router
from core.config import settings
from fastapi.templating import Jinja2Templates
from alembic import config, command
import os

templates = Jinja2Templates(directory="templates")  # регистрируем папку как папку с шаблонами джинджа


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    print("dispose engine")
    await db_helper.dispose()


main_app = FastAPI(default_response_class=ORJSONResponse, lifespan=lifespan)
main_app.include_router(
    api_router,
    # prefix=settings.api.prefix # убрать при деплое
)


# main_app.mount("/static", StaticFiles(directory="static"), name="static")


@main_app.get('/')
def start(request: Request):
    return templates.TemplateResponse('start.html', {'request': request})


@main_app.get('/adminka')
def admin(request: Request):
    return templates.TemplateResponse('/cabinets/admin.html', {'request': request})


@main_app.get('/cabinet')
def cabinet(request: Request):
    return templates.TemplateResponse('/cabinets/user.html', {'request': request})


@main_app.get('/starter')
def re_start(request: Request):
    return templates.TemplateResponse("/authuser.html", {"request": request})


if __name__ == '__main__':
    uvicorn.run("main:main_app",
                host=settings.run.host,
                port=settings.run.port,
                reload=True)
