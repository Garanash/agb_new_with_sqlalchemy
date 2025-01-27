from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.schemas.purchased import PurchasedRead, PurchasedCreate, PurchasedUpdatePartial, PurchasedBase, PurchasedDelete
from core.models import db_helper, Purchased
from api.api_v1.crud.CRUD import get_all_objects, create_new_object, update_object, get_object_by_id, delete_object

router = APIRouter(
    tags=['PurchasedBases'],
)


@router.get('/', response_model_by_alias=True)
async def get_purchaseds(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    purchaseds = await get_all_objects(session=session, model=Purchased)
    return purchaseds


@router.post("/new_purchased", response_model=None, response_model_by_alias=True)
async def create_purchased(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        purchased_create: PurchasedCreate):
    purchased = await create_new_object(session=session, object_create=purchased_create, model=Purchased)
    return purchased


@router.get('/{object_id}', response_model=None, response_model_by_alias=True)
async def search_purchased_by_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        object_id: int,
):
    object_search = await get_object_by_id(session=session, request_id=object_id, model=Purchased)
    if object_search:
        return object_search
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"object with {object_id} not found")


@router.delete('/{purchased_id}')
async def delete_purchased(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        delete_id: int,
):
    delete_purchased = await get_object_by_id(session=session, request_id=delete_id, model=Purchased)
    if not delete_purchased:
        raise HTTPException(status_code=404, detail="Purchased not found")
    await session.delete(delete_purchased)
    await session.commit()
    return {"message": f"purchased with id={delete_id} was deleted"}


@router.put('/{purchased_id}')
async def update_purchased_by_id(
        purchased_updated: PurchasedUpdatePartial,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        purchased_id: int,
):
    purchased = await get_object_by_id(request_id=purchased_id, session=session, model=Purchased)
    return await update_object(
        session=session,
        object_updating=purchased_updated,
        object_for_update=purchased,
    )
