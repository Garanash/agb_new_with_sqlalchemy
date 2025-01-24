from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, inspect
from sqlalchemy.orm import aliased
from api.api_v1.schemas.metizes import MetizCreate, MetizUpdate, MetizUpdatePartial, MetizBase
from core.models import Metiz


async def get_all_metizes(session: AsyncSession) -> Sequence[Metiz]:
    stmt = select(Metiz).order_by(Metiz.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_new_metiz(session: AsyncSession,
                           metiz_create: MetizCreate) -> Metiz:
    metiz = Metiz(**metiz_create.model_dump())
    session.add(metiz)
    await session.commit()
    # await session.refresh(user)
    return metiz


async def get_metiz_by_id(session: AsyncSession, request_id: int) -> Metiz | None:
    return await session.get(Metiz, request_id)


async def search_metiz_by_any_parameter(session: AsyncSession, request: str) -> Sequence[Metiz]:
    columns = inspect(Metiz).columns.keys()
    match_subquery = await session.execute(
        select(Metiz).where(
            any([Metiz.c[col].like(f"%{request}%") for col in columns for alias in [aliased(str(col))]])
        )
    )
    match_subquery = match_subquery.subquery()
    result = await session.execute(
        select(Metiz).outerjoin(match_subquery)
    )
    return result.scalars().all()


async def update_metiz(
        session: AsyncSession,
        metiz_for_updated: Metiz,
        metiz_updated: MetizUpdate | MetizUpdatePartial,
        partial: bool = True) -> Metiz:
    for name, value in metiz_updated.model_dump(exclude_unset=partial).items():
        setattr(metiz_for_updated, name, value)
        await session.commit()
        return metiz_for_updated


async def delete_metiz(
        session: AsyncSession,
        metiz: Metiz
) -> None:
    await session.delete(metiz)
    await session.commit()
