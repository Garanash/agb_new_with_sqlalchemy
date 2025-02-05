from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models import User


async def search_by_request(
        session: AsyncSession,
        request: str
):
    query = select(User).where(User.username == request)
    result = await session.execute(query)
    return result.scalar_one_or_none()
