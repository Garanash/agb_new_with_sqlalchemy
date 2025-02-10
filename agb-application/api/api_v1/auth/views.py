import uuid
from typing import Annotated

from authx import AuthX, AuthXConfig
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form, Cookie
from fastapi.responses import Response, RedirectResponse
from fastapi.security import HTTPBasic
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates


from api.api_v1.auth.functions import search_by_request
from api.api_v1.crud.CRUD import create_new_object
from api.api_v1.schemas.users import UserCreate
from core.loging_config import logger
from core.models import db_helper, User

config = AuthXConfig()
config.JWT_SECRET_KEY = 'PIZDEC_KAK_SECRETNO'
config.JWT_ACCESS_COOKIE_NAME = 'agb_app_token'
config.JWT_TOKEN_LOCATION = ['cookies']

security = AuthX(config=config)

router = APIRouter(prefix='/auth', tags=['Auth'])
templates = Jinja2Templates('templates')

security_log = HTTPBasic()
COOKIES = {}
COOKIE_SESSION_ID_KEY = 'agb-app-token'
ALLOWED_USERS = []


class UserLogin(BaseModel):
    username: str
    password: str


def generate_session_id():
    return uuid.uuid4().hex


@router.get('/relogin')
async def re_login(
        response: Response,
        request: Request
):
    return templates.TemplateResponse(
        'start.html',
        {
            'request': request,
            'response': response,
            'message': 'Неверное имя пользователя или пароль'
        })


@router.post('/login', response_class=RedirectResponse)
async def auth_login_with_set_cookie(
        credentials: Annotated[UserLogin, Form()],
        response: Response,
        request: Request,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],

):
    res = await search_by_request(
        request=credentials.username,
        session=session
        )
    if res:
        if credentials.password == res.password:
            token = generate_session_id()

            COOKIES[token] = {
                'username': res.username,
                'role': res.role,
                'name': res.name,
                'surname': res.surname,
                'patronymic': res.patronymic,
            }
            ALLOWED_USERS.append(credentials.username)
            logger.info(f'User {credentials.username} logged in')

            user_data = COOKIES[token]
            template_response = templates.TemplateResponse(
                'authuser.html', {
                    'request': request,
                    'response': response,
                    'username': credentials.username,
                    "userdata": user_data
                    })
            template_response.set_cookie(
                key=COOKIE_SESSION_ID_KEY,
                value=token
                )
            logger.info(f'Cookie for user {credentials.username} generated')
            return template_response
    return RedirectResponse('/auth/relogin', status_code=301)


def get_session_id(
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY)
):
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authenticated'
            )
    return COOKIES[session_id]


@router.post('/register')
async def register_user(
        user: UserCreate,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    existing_user = await search_by_request(
        request=user.username,
        session=session
        )
    if existing_user:
        logger.info(f'User {user.username} already exists')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username already registered'
            )
    await create_new_object(
        session=session,
        object_create=user,
        model=User
        )
    logger.info(f'User {user.username} registered')
    return {'message': 'User registered successfully'}


async def check_user(
        cookie_session_id: str = Cookie(None, alias=COOKIE_SESSION_ID_KEY)
        ):
    if cookie_session_id is None or cookie_session_id not in COOKIES:
        logger.info('No valid cookie provided')
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            detail='Redirecting to relogin',
            headers={"Location": "/auth/relogin"}
        )
    try:
        user_data = COOKIES[cookie_session_id]
    except Exception:
        logger.info('No valid user data found in cookie')
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            detail='Redirecting to relogin',
            headers={"Location": "/auth/relogin"}
        )

    username = user_data.get('username')
    if username not in ALLOWED_USERS:
        logger.warning(
            f'Unauthorized user {username} tried to access protected resource'
            )
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            detail='Redirecting to relogin',
            headers={"Location": "/auth/relogin"}
        )
    return user_data


@router.get('/logout')
async def logout(
        response: Response,
        request: Request
        ):
    cookie_session_id = get_session_id(
        session_id=request.cookies.get(COOKIE_SESSION_ID_KEY)
        )
    ALLOWED_USERS.remove(cookie_session_id['username'])
    logger.info(f'User {cookie_session_id["username"]} logged out')
    template_response = templates.TemplateResponse(
        'start.html',
        {
            'request': request,
            'response': response,
        })
    template_response.delete_cookie(key=COOKIE_SESSION_ID_KEY)
    logger.info(f'Cookie for user {cookie_session_id["username"]} deleted')
    return template_response
