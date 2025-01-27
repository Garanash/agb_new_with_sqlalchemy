from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.schemas.purchased_hydroperforator import PurchasedHydroperforatorRead, PurchasedHydroperforatorCreate, \
    PurchasedHydroperforatorUpdatePartial, PurchasedHydroperforatorBase, PurchasedHydroperforatorDelete
from core.models import db_helper, PurchasedHydroperforator
from api.api_v1.crud.CRUD import get_all_objects, create_new_object, update_object, get_object_by_id, delete_object, \
    search_by_request

router = APIRouter(
    tags=['PurchasedHydroperforatorBases'],
)


@router.get('/', response_model_by_alias=True)
async def get_purchased_hydroperforator(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    purchased_hydroperforator = await get_all_objects(session=session, model=PurchasedHydroperforator)
    return purchased_hydroperforator


@router.post("/new_purchased_hydroperforator", response_model=None, response_model_by_alias=True)
async def create_purchased_hydroperforator(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        purchased_hydroperforator_create: PurchasedHydroperforatorCreate):
    purchased_hydroperforator = await create_new_object(session=session, object_create=purchased_hydroperforator_create,
                                                        model=PurchasedHydroperforator)
    return purchased_hydroperforator


@router.get('/{object_id}', response_model=None, response_model_by_alias=True)
async def search_purchased_hydroperforator_by_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        object_id: int,
):
    object_search = await get_object_by_id(session=session, request_id=object_id, model=PurchasedHydroperforator)
    if object_search:
        return object_search
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"object with {object_id} not found")


@router.delete('/{purchased_hydroperforator_id}')
async def delete_purchased_hydroperforator(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        delete_id: int,
):
    delete_purchased_hydroperforator = await get_object_by_id(session=session, request_id=delete_id,
                                                              model=PurchasedHydroperforator)
    if not delete_purchased_hydroperforator:
        raise HTTPException(status_code=404, detail="PurchasedHydroperforator not found")
    await session.delete(delete_purchased_hydroperforator)
    await session.commit()
    return {"message": f"purchased_hydroperforator with id={delete_id} was deleted"}


@router.put('/{purchased_hydroperforator_id}')
async def update_purchased_hydroperforator_by_id(
        purchased_hydroperforator_updated: PurchasedHydroperforatorUpdatePartial,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        purchased_hydroperforator_id: int,
):
    purchased_hydroperforator = await get_object_by_id(request_id=purchased_hydroperforator_id, session=session,
                                                       model=PurchasedHydroperforator)
    return await update_object(
        session=session,
        object_updating=purchased_hydroperforator_updated,
        object_for_update=purchased_hydroperforator,
    )


@router.get('/s/{request_item}')
async def search_purchasedhydro_by_request(
        request_item: str,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    return await search_by_request(request=request_item, session=session, model=PurchasedHydroperforator)