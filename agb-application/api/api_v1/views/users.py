from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.schemas.users import UserRead, UserCreate, UserUpdatePartial, UserBase, UserDelete
from core.models import db_helper, User
from api.api_v1.crud.CRUD import get_all_objects, create_new_object, update_object, get_object_by_id, delete_object

router = APIRouter(
    tags=['UserBases'],
)


@router.get('/', response_model_by_alias=True)
async def get_users(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    users = await get_all_objects(session=session, model=User)
    return users


@router.post("/new_user", response_model=None, response_model_by_alias=True)
async def create_user(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user_create: UserCreate):
    user = await create_new_object(session=session, object_create=user_create, model=User)
    return user


@router.get('/{object_id}', response_model=None, response_model_by_alias=True)
async def search_user_by_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        object_id: int,
):
    object_search = await get_object_by_id(session=session, request_id=object_id, model=User)
    if object_search:
        return object_search
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"object with {object_id} not found")


@router.delete('/{user_id}')
async def delete_user(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        delete_id: int,
):
    delete_user = await get_object_by_id(session=session, request_id=delete_id, model=User)
    if not delete_user:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(delete_user)
    await session.commit()
    return {"message": f"user with id={delete_id} was deleted"}


@router.put('/{user_id}')
async def update_user_by_id(
        user_updated: UserUpdatePartial,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user_id: int,
):
    user = await get_object_by_id(request_id=user_id, session=session, model=User)
    return await update_object(
        session=session,
        object_updating=user_updated,
        object_for_update=user,
    )
