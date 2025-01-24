from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.schemas.RWD import RWDCreate, RWDDelete, RWDRead, RWDUpdate, RWDUpdatePartial, RWDBase
from core.models import db_helper, RWD
from api.api_v1.crud.CRUD import get_all_objects, create_new_object, update_object, get_object_by_id, delete_object

router = APIRouter(
    tags=['RWDBases'],
)


@router.get('/', response_model_by_alias=True)
async def get_rwd_item(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    rwd_item = await get_all_objects(session=session, model=RWD)
    return rwd_item


@router.post("/new_rwd_item", response_model=None, response_model_by_alias=True)
async def create_rwd_item(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        rwd_item_create: RWDCreate):
    rwd_item = await create_new_object(session=session, object_create=rwd_item_create, model=RWD)
    return rwd_item


@router.get('/{rwd_item_id}', response_model=None, response_model_by_alias=True)
async def search_rwd_item_by_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        rwd_item_id: int,
):
    object_search = await get_object_by_id(session=session, request_id=rwd_item_id, model=RWD)
    if object_search:
        return object_search
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"object with {rwd_item_id} not found")


@router.delete('/{rwd_item_id}')
async def delete_rwd_item(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        delete_id: int,
):
    delete_rwd_item = await get_object_by_id(session=session, request_id=delete_id, model=RWD)
    if not delete_rwd_item:
        raise HTTPException(status_code=404, detail="RWD not found")
    await session.delete(delete_rwd_item)
    await session.commit()
    return {"message": f"rwd_item with id={delete_id} was deleted"}


@router.put('/{rwd_item_id}')
async def update_rwd_item_by_id(
        rwd_item_updated: RWDUpdatePartial,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        rwd_item_id: int,
):
    rwd_item = await get_object_by_id(request_id=rwd_item_id, session=session, model=RWD)
    return await update_object(
        session=session,
        object_updating=rwd_item_updated,
        object_for_update=rwd_item,
    )
