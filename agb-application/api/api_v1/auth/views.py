import uuid
from typing import Annotated
from time import time

from fastapi import  APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates
from api.api_v1.auth.functions import search_by_request
from core.models import db_helper, User
from api.api_v1.crud.CRUD import create_new_object
from api.api_v1.schemas.users import UserCreate
from authx import AuthX, AuthXConfig

config = AuthXConfig()
config.JWT_SECRET_KEY = "PIZDEC SECRET"
config.JWT_ACCESS_COOKIE_NAME = "agb-app-token"
config.JWT_TOKEN_LOCATION = ['cookies']

security = AuthX(config=config)

router = APIRouter(prefix="/auth", tags=['Auth'])
templates = Jinja2Templates('templates')

security_log = HTTPBasic()


def generate_session_id():
    return uuid.uuid4().hex


@router.post("/login")
async def auth_login_cookie(
        response: Response,
        request: Request,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        credentials: Annotated[HTTPBasicCredentials, Depends(security_log)]
):
    res = await search_by_request(request=credentials.username, session=session)
    if res:
        if credentials.password == res.password:
            token = security.create_access_token(uid=res.username)
            response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
            return templates.TemplateResponse('authuser.html',
                                              {"request": request,
                                               "response": response,
                                               "username": credentials.username,
                                               "password": credentials.password
                                               })
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")


@router.post("/register")
async def register_user(
        user: UserCreate,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    # Проверяем, существует ли уже пользователь
    existing_user = await search_by_request(request=user.username, session=session)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    # Создаем нового пользователя
    await create_new_object(session=session, object_create=user, model=User)
    return {"message": "User registered successfully"}


# Эндпоинт для выхода из системы
@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
    return {"message": "Successfully logged out"}
