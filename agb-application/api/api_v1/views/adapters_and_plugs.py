from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.schemas.adapters_and_plugs import AdapterAndPlugsRead, AdapterAndPlugsCreate, \
    AdapterAndPlugsUpdatePartial, AdapterAndPlugsBase, AdapterAndPlugsDelete
from core.models import db_helper, AdaptersAndPlugs
from api.api_v1.crud.CRUD import get_all_objects, create_new_object, update_object, get_object_by_id, delete_object, \
    search_by_request

router = APIRouter(
    tags=['AdapterAndPlugsBases'],
)


@router.get('/', response_model_by_alias=True)
async def get_adapters_and_plugss(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    adapters_and_plugs = await get_all_objects(session=session, model=AdaptersAndPlugs)
    return adapters_and_plugs


@router.post("/new_adapters_and_plugs", response_model=None, response_model_by_alias=True)
async def create_adapters_and_plugs(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        adapters_and_plugs_create: AdapterAndPlugsCreate):
    adapters_and_plugs = await create_new_object(session=session, object_create=adapters_and_plugs_create,
                                                 model=AdaptersAndPlugs)
    return adapters_and_plugs


@router.get('/{object_id}', response_model=None, response_model_by_alias=True)
async def search_adapters_and_plugs_by_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        object_id: int,
):
    object_search = await get_object_by_id(session=session, request_id=object_id, model=AdaptersAndPlugs)
    if object_search:
        return object_search
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"object with {object_id} not found")


@router.delete('/{adapters_and_plugs_id}')
async def delete_adapters_and_plugs(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        delete_id: int,
):
    delete_adapters_and_plugs = await get_object_by_id(session=session, request_id=delete_id, model=AdaptersAndPlugs)
    if not delete_adapters_and_plugs:
        raise HTTPException(status_code=404, detail="AdapterAndPlugs not found")
    await session.delete(delete_adapters_and_plugs)
    await session.commit()
    return {"message": f"adapters_and_plugs with id={delete_id} was deleted"}


@router.put('/{adapters_and_plugs_id}')
async def update_adapters_and_plugs_by_id(
        adapters_and_plugs_updated: AdapterAndPlugsUpdatePartial,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        adapters_and_plugs_id: int,
):
    adapters_and_plugs = await get_object_by_id(request_id=adapters_and_plugs_id, session=session,
                                                model=AdaptersAndPlugs)
    return await update_object(
        session=session,
        object_updating=adapters_and_plugs_updated,
        object_for_update=adapters_and_plugs,
    )


@router.get('/s/{request_item}')
async def search_adapter_by_request(
        request_item: str,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    return await search_by_request(request=request_item, session=session, model=AdaptersAndPlugs)
