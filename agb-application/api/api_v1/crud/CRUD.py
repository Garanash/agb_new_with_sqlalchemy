from typing import Optional

from sqlalchemy import select, Sequence, text, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.inspection import inspect

from api.api_v1.schemas import UserUpdatePartial, UserCreate, MetizCreate, RWDCreate, RWDUpdatePartial, \
    MetizUpdatePartial, ProjectUpdatePartial, ProjectCreate, PurchasedUpdatePartial, PurchasedCreate, \
    PurchasedHydroperforatorCreate, PurchasedHydroperforatorUpdatePartial, AdapterAndPlugsUpdatePartial, \
    AccordingToTheDrawCreate, AccordingToTheDrawUpdatePartial, AdapterAndPlugsCreate
from core.models import Metiz, User, RWD, Project, AdaptersAndPlugs, AccordingToTheDrawing, Purchased, \
    PurchasedHydroperforator


async def get_all_objects(session: AsyncSession, model: Optional[type[
    User | Metiz | RWD | Project | AdaptersAndPlugs | AccordingToTheDrawing | Purchased | PurchasedHydroperforator]]):
    stmt = select(model).order_by(model.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_object_by_id(session: AsyncSession, model: Optional[type[
    User | Metiz | RWD | Project | AdaptersAndPlugs | AccordingToTheDrawing | Purchased | PurchasedHydroperforator]],
                           request_id: int):
    return await session.get(model, request_id)


async def create_new_object(session: AsyncSession,
                            model: Optional[type[
                                User | Metiz | RWD | Project | AdaptersAndPlugs | AccordingToTheDrawing | Purchased | PurchasedHydroperforator]],
                            object_create: Optional[
                                UserCreate | MetizCreate | RWDCreate | ProjectCreate | PurchasedCreate | PurchasedHydroperforatorCreate | AdapterAndPlugsCreate | AccordingToTheDrawCreate]
                            ):
    obj = model(**object_create.model_dump())
    session.add(obj)
    await session.commit()
    return obj


async def update_object(
        session: AsyncSession,
        object_for_update: Optional[
            User | Metiz | RWD | Project | AdaptersAndPlugs | AccordingToTheDrawing | Purchased | PurchasedHydroperforator],
        object_updating: Optional[
            UserUpdatePartial | MetizUpdatePartial | RWDUpdatePartial | ProjectUpdatePartial | PurchasedUpdatePartial | PurchasedHydroperforatorUpdatePartial | AdapterAndPlugsUpdatePartial | AccordingToTheDrawUpdatePartial],
        partial: bool = True
):
    for name, value in object_updating.model_dump(exclude_unset=partial).items():
        setattr(object_for_update, name, value)
    await session.commit()
    return object_for_update


async def delete_object(
        session: AsyncSession,
        model: Optional[type[
            User | Metiz | RWD | Project | AdaptersAndPlugs | AccordingToTheDrawing | Purchased | PurchasedHydroperforator | None]]
) -> None:
    await session.delete(model)
    await session.commit()


async def search_by_request(
        session: AsyncSession,
        model: Optional[type[
            User | Metiz | RWD | Project | AdaptersAndPlugs | AccordingToTheDrawing | Purchased | PurchasedHydroperforator]],
        request: str
):
    attributes = [attr.key for attr in inspect(model).mapper.attrs]
    attributes.pop(attributes.index('marked_for_deletion'))
    attributes.pop(attributes.index('id'))
    conditions = [getattr(model, attr).ilike(f"%{request}%") for attr in attributes]
    query = select(model).where(or_(*conditions))
    result = await session.execute(query)
    return result.scalars().all()
