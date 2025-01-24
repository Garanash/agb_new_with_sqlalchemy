from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.api_v1.schemas.users import UserCreate, UserUpdate, UserUpdatePartial, UserBase
from core.models import User


async def get_all_users(session: AsyncSession) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_new_user(session: AsyncSession,
                          user_create: UserCreate) -> User:
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    # await session.refresh(user)
    return user


async def get_user_by_id(session: AsyncSession, request_id: int) -> User | None:
    return await session.get(User, request_id)


async def update_user(
        session: AsyncSession,
        user_for_updated: User,
        user_updated: UserUpdate | UserUpdatePartial,
        partial: bool = False) -> User:
    for name, value in user_updated.model_dump(exclude_unset=partial).items():
        setattr(user_for_updated, name, value)
        await session.commit()
        return user_for_updated


async def delete_user(
        session: AsyncSession,
        user: User
) -> None:
    await session.delete(user)
    await session.commit()
