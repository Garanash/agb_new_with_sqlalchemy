from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.api_v1.schemas import UserUpdatePartial, UserCreate, MetizCreate, RWDCreate, RWDUpdatePartial, \
    MetizUpdatePartial, ProjectUpdatePartial, ProjectCreate
from core.models import Metiz, User, RWD, Project
from typing import Optional


async def get_all_objects(session: AsyncSession, model: Optional[type[User | Metiz | RWD | Project]]):
    stmt = select(model).order_by(model.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_object_by_id(session: AsyncSession, model: Optional[type[User | Metiz | RWD | Project]], request_id: int):
    return await session.get(model, request_id)


async def create_new_object(session: AsyncSession,
                            model: Optional[type[User | Metiz | RWD | Project]],
                            object_create: Optional[UserCreate | MetizCreate | RWDCreate | ProjectCreate]
                            ):
    obj = model(**object_create.model_dump())
    session.add(obj)
    await session.commit()
    return obj


async def update_object(
        session: AsyncSession,
        object_for_update: Optional[User | Metiz | RWD | Project],
        object_updating: Optional[UserUpdatePartial | MetizUpdatePartial | RWDUpdatePartial | ProjectUpdatePartial],
        partial: bool = True
):
    for name, value in object_updating.model_dump(exclude_unset=partial).items():
        setattr(object_for_update, name, value)
    await session.commit()
    return object_for_update


async def delete_object(
        session: AsyncSession,
        model: Optional[type[User | Metiz | RWD | Project | None]]
) -> None:
    await session.delete(model)
    await session.commit()
