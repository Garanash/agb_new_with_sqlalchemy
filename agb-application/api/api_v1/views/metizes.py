# from typing import Annotated
#
# from fastapi import APIRouter, Depends
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from api.api_v1.crud.metizes import get_all_metizes, create_new_metiz, get_metiz_by_id, update_metiz
# from api.api_v1.schemas.metizes import MetizRead, MetizCreate, MetizUpdatePartial, MetizBase, MetizDelete
# from core.models import db_helper, Metiz
# from .dependencies import metiz_by_id
#
# router = APIRouter(
#     tags=['MetizBases'],
# )
#
#
# @router.get('/', response_model=list[MetizBase])
# async def get_metizes(
#         session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
# ):
#     metizs = await get_all_metizes(session=session)
#     return metizs
#
#
# @router.post("/new_metiz", response_model=MetizBase)
# async def create_metiz(
#         session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
#         metiz_create: MetizCreate):
#     metiz = await create_new_metiz(session=session, metiz_create=metiz_create)
#     return metiz
#
#
# @router.get('/{metiz_id}', response_model=MetizBase)
# async def search_metiz_by_id(
#         metiz: MetizRead = Depends(metiz_by_id)
# ):
#     return metiz
#
#
# @router.put('/{metiz_id}', response_model=MetizBase)
# async def update_metiz_by_id(
#         metiz_updated: MetizUpdatePartial,
#         session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
#         metiz_for_update: MetizRead = Depends(metiz_by_id),
# ):
#     return await update_metiz(
#         session=session,
#         metiz_updated=metiz_updated,
#         metiz_for_updated=metiz_for_update,
#         partial=True
#     )
#
#
# @router.delete('/{metiz_id}')
# async def delete_metiz(
#         session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
#         delete_metiz: MetizDelete = Depends(metiz_by_id),
# ):
#     await session.delete(delete_metiz)
#     await session.commit()
#     return {"success": "true"}
