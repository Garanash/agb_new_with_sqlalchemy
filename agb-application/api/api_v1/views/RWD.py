from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.schemas.RWD import RWDCreate, RWDUpdatePartial
from api.api_v1.crud.CRUD import get_all_objects, create_new_object, update_object, get_object_by_id, delete_object, \
    search_by_request
from api.api_v1.auth.views import check_user
from core.models import db_helper, RWD


templates = Jinja2Templates('templates')
router = APIRouter(
    tags=['RWDBases'],
)


@router.get('/RWDs',
            response_model_by_alias=True,
            dependencies=[Depends(check_user)])
async def get_rwd(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request
):
    """
    Вывод всех РВД в таблице
    :parameter:
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    rwd = await get_all_objects(
        session=session,
        model=RWD
        )
    return templates.TemplateResponse('/search/rwd.html',
                                      {'request': request,
                                       'rwd': rwd})


@router.get('/',
            response_model_by_alias=True,
            dependencies=[Depends(check_user)])
async def get_rwd_item(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    """
    Вывод одного РВД по его id
    :parameter:
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    rwd_item = await get_all_objects(
        session=session,
        model=RWD
        )
    return rwd_item


@router.get('/addnew',
            dependencies=[Depends(check_user)])
async def add_new_rwd(request: Request):
    """
    Добавление нового РВД
    :parameter:
    request: запрос от пользователя
    session: сессия в асинхронную базу данных
    """
    return templates.TemplateResponse('/addnew/add_new_rwd.html',
                                      {'request': request,
                                       'current_datetime': datetime.now().strftime('%Y-%m-%d %H:%M')})


@router.get('/patch/{item_id}',
            dependencies=[Depends(check_user)])
async def patch_rwd_by_id(request: Request,
                          item_id: int,
                          session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    """
    Редактирование РВД по его id
    :parameter:
    request: запрос от пользователя
    item_id: id РВД для редактирования
    """
    patch_item = await get_object_by_id(
        session=session,
        model=RWD,
        request_id=item_id
        )

    return templates.TemplateResponse('/patch/patch_rwd.html',
                                      {'request': request,
                                       'current_datetime': datetime.now().strftime('%Y-%m-%d %H:%M'),
                                       'item': patch_item})


@router.post('/patch',
             response_class=RedirectResponse,
             dependencies=[Depends(check_user)])
async def patch_rwd(
        patch_item: Annotated[RWDUpdatePartial, Form()],
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request
        ):
    """
    Редактирование РВД по его id
    :parameter:
    patch_item: данные для редактирования
    session: сессия в асинхронную базу данных
    """
    object_for_update = await get_object_by_id(
        request_id=patch_item.id,
        session=session,
        model=RWD
        )
    await update_object(
        session=session,
        object_for_update=object_for_update,
        object_updating=patch_item,
        partial=True
        )
    return RedirectResponse('/RWD/RWDs',
                            status_code=status.HTTP_301_MOVED_PERMANENTLY)


@router.post('/create',
             response_model=None,
             response_model_by_alias=True,
             response_class=RedirectResponse,
             dependencies=[Depends(check_user)])
async def create_rwd(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        rwd_create: Annotated[RWDCreate, Form()],
        request: Request
        ):
    """
    создание нового РВД
    :parameter:
    rwd_create: данные для создания
    session: сессия в асинхронную базу данных
    """
    try:
        rwd = await create_new_object(
            session=session,
            object_create=rwd_create,
            model=RWD
            )
        return RedirectResponse('/RWD/RWDs',
                                status_code=status.HTTP_301_MOVED_PERMANENTLY)

    except BaseException:
        return templates.TemplateResponse('/search/rwd.html',
                                          {'request': request,
                                           'message': 'Такая деталь уже существует'})


@router.get('/search',
            dependencies=[Depends(check_user)])
async def search_rwd_by_request(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request
):
    """
    Поиск РВД по детальному ключу
    :parameter:
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    search_item = request.query_params.get('main_input')
    res_search = await search_by_request(
        request=search_item,
        session=session,
        model=RWD
        )
    return templates.TemplateResponse('/finded/rwds.html',
                                      {'request': request,
                                       'rwds': res_search})


@router.get('/{rwd_item_id}',
            response_model=None,
            response_model_by_alias=True,
            dependencies=[Depends(check_user)])
async def search_rwd_item_by_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        rwd_item_id: int,
):
    """
    Поиск РВД по его id
    :parameter:
    session: сессия в асинхронную базу данных
    rwd_item_id: id РВД для поиска
    """
    object_search = await get_object_by_id(
        session=session,
        request_id=rwd_item_id,
        model=RWD
        )
    if object_search:
        return object_search
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'object with {rwd_item_id} not found'
        )


@router.delete('/{rwd_item_id}',
               dependencies=[Depends(check_user)])
async def delete_rwd_item(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        delete_id: int,
):
    """
    Удаление РВД по его id
    :parameter:
    session: сессия в асинхронную базу данных
    delete_id: id РВД для удаления
    """
    delete_rwd_item = await get_object_by_id(
        session=session,
        request_id=delete_id,
        model=RWD
        )
    if not delete_rwd_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='RWD not found'
            )
    await session.delete(delete_rwd_item)
    await session.commit()
    return {'message': f'rwd_item with id={delete_id} was deleted'}


@router.put('/{rwd_item_id}',
            dependencies=[Depends(check_user)])
async def update_rwd_item_by_id(
        rwd_item_updated: RWDUpdatePartial,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        rwd_item_id: int,
):
    """
    Редактирование РВД по его id
    :parameter:
    rwd_item_updated: данные для редактирования
    session: сессия в асинхронную базу данных
    rwd_item_id: id РВД для редактирования
    """
    rwd_item = await get_object_by_id(
        request_id=rwd_item_id,
        session=session,
        model=RWD
        )
    return await update_object(
        session=session,
        object_updating=rwd_item_updated,
        object_for_update=rwd_item,
    )


# @router.get('/s/{request_item}')
# async def search_rwd_by_request(
#         request_item: str,
#         session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
# ):
#     return await search_by_request(request=request_item, session=session, model=RWD)