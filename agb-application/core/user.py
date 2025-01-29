from typing import Optional, Union

from pydantic import BaseModel
from fastapi import Depends, Request, HTTPException, Response
from fastapi_users import (
    BaseUserManager, FastAPIUsers, IntegerIDMixin, InvalidPasswordException
)
from fastapi_users.authentication import (
    AuthenticationBackend,  JWTStrategy, CookieTransport
)
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper
from core.models.user import User
from api.api_v1.schemas.users import UserCreate


async def get_user_db(
        session: AsyncSession = Depends(db_helper.session_getter)
        ):
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = CookieTransport(
    cookie_name="agb-app-token",
    cookie_max_age=3600,
    cookie_secure=True,
    cookie_samesite="Lax"
    )


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason='Password should be at least 8 characters'
            )
        # if user.email in password:
        #     raise InvalidPasswordException(
        #         reason='Password should not contain e-mail'
        #     )

    async def on_after_register(
            self, user: User, request: Optional[Request] = None
    ):
        print(f'Пользователь {user.username} зарегистрирован.')

    async def on_after_login(
            self,
            user,
            request: Optional[Request] = None,
            response: Optional[Response] = None
            ):
        response.set_cookie(
            key='agb-app-token',
            value=user.username,
            expires_in=3600,
            secure=True,
            samesite='Lax'
            )
        return await super().on_after_login(user, request, response)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
