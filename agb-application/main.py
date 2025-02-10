import logging
import pathlib
from logging.handlers import RotatingFileHandler
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from fastapi.templating import Jinja2Templates

from api import router as api_router
from core.config import settings
from core.models import db_helper

templates = Jinja2Templates(directory='templates')

logger = logging.getLogger(__name__)
handler = RotatingFileHandler('logger.log')
logger.setLevel('DEBUG')
logger.addHandler(handler)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    print('dispose engine')
    await db_helper.dispose()


main_app = FastAPI(default_response_class=ORJSONResponse, lifespan=lifespan)
main_app.include_router(
    api_router,
    # prefix=settings.api.prefix # убрать при деплое
)


# main_app.mount("/static", StaticFiles(directory="static"), name="static")


@main_app.get('/')
def start(request: Request):
    logger.info('Start page')
    return templates.TemplateResponse('start.html', {'request': request})


@main_app.get('/adminka')
def admin(request: Request):
    logger.info('Admin page')
    return templates.TemplateResponse('/cabinets/admin.html', {'request': request})


@main_app.get('/cabinet')
def cabinet(request: Request):
    logger.info('Cabinet page')
    return templates.TemplateResponse('/cabinets/user.html', {'request': request})


@main_app.get('/starter')
def re_start(request: Request):
    logger.info('Re-start page')
    return templates.TemplateResponse('/authuser.html', {'request': request})


if __name__ == '__main__':
    logger.info('Run application')
    cwd = pathlib.Path(__file__).parent.resolve()
    uvicorn.run("main:main_app",
                host=settings.run.host,
                port=settings.run.port,
                reload=True,
                log_level='info',
                log_config=f'{cwd}/log.ini')
