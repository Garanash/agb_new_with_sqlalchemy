from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.crud.user import user_crud
from api.api_v1.schemas.users import UserCreate, UserUpdatePartial
from core.models import db_helper, User

router = APIRouter(
    tags=['UserBases'],
)


@router.get('/',
            response_model_by_alias=True)
async def get_users(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    users = await user_crud.get_multi(session=session)
    return users


@router.post("/new_user",
             response_model=None,
             response_model_by_alias=True)
async def create_user(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user_create: UserCreate
):
    user = await user_crud.create(session=session, obj_in=user_create)
    return user


@router.get('/{object_id}',
            response_model=None,
            response_model_by_alias=True)
async def search_user_by_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        object_id: int,
):
    object_search = await check_user_exists(session=session, user_id=object_id)
    return object_search


@router.delete('/{user_id}')
async def delete_user(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        delete_id: int,
):
    delete_user = await check_user_exists(session=session, user_id=delete_id)
    deleted_user = await user_crud.remove(session=session, db_obj=delete_user)
    return deleted_user


@router.put('/{user_id}')
async def update_user_by_id(
        user_update: UserUpdatePartial,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user_id: int,
):
    user = await check_user_exists(session=session, user_id=user_id)
    return await user_crud.update(
        session=session,
        db_obj=user,
        obj_in=user_update
    )


@router.get('/s/{request_item}')
async def search_user_by_request(
        request: Request,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    search_item = request.query_params.get('main_input')
    res_search = await user_crud.search(
        request=search_item,
        session=session
        )
    return res_search


async def check_user_exists(
    user_id: int,
    session: AsyncSession
) -> User:
    """
    Проверка существования пользователя по id
    :parameter:
    user_id: id детали
    session: сессия в асинхронную базу данных
    """
    user = await user_crud.get(
        user_id, session
    )
    match user:
        case None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Не найдено!'
            )
    return user
