from typing import Annotated

from fastapi import Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.crud.users import get_user_by_id
from api.api_v1.crud.metizes import get_metiz_by_id
from core.models import db_helper, User, Metiz


async def user_by_id(
        user_id: Annotated[int, Path],
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> User:
    user = await get_user_by_id(session=session, request_id=user_id)
    if user is not None:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found!",
    )


async def metiz_by_id(
        metiz_id: Annotated[int, Path],
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> Metiz:
    metiz = await get_metiz_by_id(session=session, request_id=metiz_id)
    if metiz is not None:
        return metiz
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"metiz {metiz_id} not found!",
    )
