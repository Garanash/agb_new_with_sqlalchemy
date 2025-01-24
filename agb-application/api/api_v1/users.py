from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.crud.users import get_all_users, create_new_user, get_user_by_id, update_user
from api.api_v1.schemas.users import UserRead, UserCreate, UserUpdatePartial, UserBase, UserDelete
from core.models import db_helper, User
from .dependencies import user_by_id

router = APIRouter(
    tags=['UserBases'],
)


@router.get('/', response_model=list[UserBase])
async def get_users(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    users = await get_all_users(session=session)
    return users


@router.post("/new_user", response_model=UserBase)
async def create_user(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user_create: UserCreate):
    user = await create_new_user(session=session, user_create=user_create)
    return user


@router.get('/{user_id}', response_model=UserBase)
async def search_user_by_id(
        user: UserRead = Depends(user_by_id)
):
    return user


@router.put('/{user_id}', response_model=UserBase)
async def update_user_by_id(
        user_updated: UserUpdatePartial,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user_for_update: UserRead = Depends(user_by_id),
):
    return await update_user(
        session=session,
        user_updated=user_updated,
        user_for_updated=user_for_update,
        partial=True
    )


@router.delete('/{user_id}')
async def delete_user(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        delete_user: UserDelete = Depends(user_by_id),
):
    await session.delete(delete_user)
    await session.commit()
    return {"success": "true"}
