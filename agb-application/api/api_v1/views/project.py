from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.views import check_user
from api.api_v1.schemas.project import ProjectRead, ProjectCreate, ProjectUpdatePartial, ProjectBase, ProjectDelete
from core.models import db_helper, Project
from api.api_v1.crud.CRUD import get_all_objects, create_new_object, update_object, get_object_by_id, delete_object, \
    search_by_request

router = APIRouter(
    tags=['ProjectBases'],
    dependencies=[Depends(check_user)]
)


@router.get('/', response_model_by_alias=True)
async def get_project(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    project = await get_all_objects(session=session, model=Project)
    return project


@router.post('/new_project', response_model=None, response_model_by_alias=True)
async def create_project(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        project_create: ProjectCreate):
    project = await create_new_object(session=session, object_create=project_create, model=Project)
    return project


@router.get('/{object_id}', response_model=None, response_model_by_alias=True)
async def search_project_by_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        object_id: int,
):
    object_search = await get_object_by_id(session=session, request_id=object_id, model=Project)
    if object_search:
        return object_search
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'object with {object_id} not found')


@router.delete('/{project_id}')
async def delete_project(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        delete_id: int,
):
    delete_project = await get_object_by_id(session=session, request_id=delete_id, model=Project)
    if not delete_project:
        raise HTTPException(status_code=404, detail='Project not found')
    await session.delete(delete_project)
    await session.commit()
    return {'message': f'project with id={delete_id} was deleted'}


@router.put('/{project_id}')
async def update_project_by_id(
        project_updated: ProjectUpdatePartial,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        project_id: int,
):
    project = await get_object_by_id(request_id=project_id, session=session, model=Project)
    return await update_object(
        session=session,
        object_updating=project_updated,
        object_for_update=project,
    )


@router.get('/s/{request_item}')
async def search_project_by_request(
        request_item: str,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    return await search_by_request(request=request_item, session=session, model=Project)
