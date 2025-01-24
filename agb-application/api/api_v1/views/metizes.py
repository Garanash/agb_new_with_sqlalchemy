from typing import Annotated

from asyncpg import UniqueViolationError
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.schemas.metizes import MetizRead, MetizCreate, MetizUpdatePartial, MetizBase, MetizDelete, MetizUpdate
from core.models import db_helper, Metiz
from api.api_v1.crud.CRUD import get_all_objects, create_new_object, update_object, get_object_by_id, delete_object

router = APIRouter(
    tags=['MetizBases'],
)


@router.get('/', response_model_by_alias=True)
async def get_metizes(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    metiz = await get_all_objects(session=session, model=Metiz)
    return metiz


@router.post("/new_metiz", response_model=None, response_model_by_alias=True)
async def create_metiz(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        metiz_create: MetizCreate):
    try:
        metiz = await create_new_object(session=session, object_create=metiz_create, model=Metiz)
        return metiz
    except BaseException:
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="metiz already exists")


@router.get('/{object_id}', response_model=None, response_model_by_alias=True)
async def search_metiz_by_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        object_id: int,
):
    object_search = await get_object_by_id(session=session, request_id=object_id, model=Metiz)
    if object_search:
        return object_search
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"object with {object_id} not found")


@router.delete('/{metiz_id}')
async def delete_metiz(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        delete_id: int,
):
    delete_metiz = await get_object_by_id(session=session, request_id=delete_id, model=Metiz)
    if not delete_metiz:
        raise HTTPException(status_code=404, detail="Metiz not found")
    await session.delete(delete_metiz)
    await session.commit()
    return {"message": f"metiz with id={delete_id} was deleted"}


@router.put('/{metiz_id}')
async def update_metiz_by_id(
        metiz_updated: MetizUpdatePartial,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        metiz_id: int,
):
    metiz = await get_object_by_id(request_id=metiz_id, session=session, model=Metiz)
    return await update_object(
        session=session,
        object_updating=metiz_updated,
        object_for_update=metiz,
    )
