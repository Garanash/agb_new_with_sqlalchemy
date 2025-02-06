from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.schemas.metizes import MetizCreate, MetizUpdatePartial
from api.api_v1.crud.CRUD import get_all_objects, create_new_object, update_object, get_object_by_id, delete_object, \
    search_by_request
from api.api_v1.auth.views import check_user
from core.models import db_helper, Metiz

templates = Jinja2Templates('templates')

router = APIRouter(
    tags=['MetizBases'],
)


@router.get('/metizes',
            response_model_by_alias=True,
            dependencies=[Depends(check_user)])
async def get_metizes(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request
):
    """
    Вывод всех метизов в таблице
    :parameter:
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    metiz = await get_all_objects(
        session=session,
        model=Metiz
        )
    return templates.TemplateResponse('/search/metizes.html',
                                      {'request': request,
                                       'metizes': metiz})


@router.get('/addnew',
            dependencies=[Depends(check_user)])
async def add_new_metiz(request: Request):
    """
    Добавление нового метиза
    :parameter:
    request: запрос от пользователя
    """
    return templates.TemplateResponse('/addnew/add_new_metiz.html',
                                      {'request': request,
                                       'current_datetime': datetime.now().strftime('%Y-%m-%d %H:%M')})


@router.get("/patch/{item_id}",
            dependencies=[Depends(check_user)])
async def patch_metiz_by_id(request: Request,
                            item_id: int,
                            session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    patch_item = await get_object_by_id(
        session=session,
        model=Metiz,
        request_id=item_id
        )

    return templates.TemplateResponse('/patch/patch_metiz.html',
                                      {'request': request,
                                       'current_datetime': datetime.now().strftime("%Y-%m-%d %H:%M"),
                                       'item': patch_item})


@router.post('/patch',
             response_class=RedirectResponse,
             dependencies=[Depends(check_user)])
async def patch_metizes(
        patch_item: Annotated[MetizUpdatePartial, Form()],
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request
        ):
    """
    Обновление детали
    :parameter:
    patch_item: данные для изменения
    session: сессия в асинхронную базу данных
    """
    object_for_update = await get_object_by_id(
        request_id=patch_item.id,
        session=session,
        model=Metiz
        )
    await update_object(
        session=session,
        object_for_update=object_for_update,
        object_updating=patch_item,
        partial=True
        )
    return RedirectResponse('/metiz/metizes',
                            status_code=status.HTTP_301_MOVED_PERMANENTLY)


@router.post("/create",
             response_model=None,
             response_model_by_alias=True,
             response_class=RedirectResponse,
             dependencies=[Depends(check_user)])
async def create_metiz(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        metiz_create: Annotated[MetizCreate, Form()],
        request: Request):
    """
    Создание новой детали
    :parameter:
    session: сессия в асинхронную базу данных
    metiz_create: данные для создания
    request: запрос от пользователя
    """
    metiz_check = await get_all_objects(
        session=session,
        model=Metiz,
        filter_by=Metiz.name == metiz_create.name
        )
    if metiz_check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Такая деталь уже существует'
            )
    try:
        metiz = await create_new_object(
            session=session,
            object_create=metiz_create,
            model=Metiz
            )
        return RedirectResponse('/metiz/metizes',
                                status_code=status.HTTP_301_MOVED_PERMANENTLY)

    except BaseException:
        return templates.TemplateResponse('/search/metizes.html',
                                          {'request': request,
                                           "message": 'Такая деталь уже существует'})


@router.get('/search',
            dependencies=[Depends(check_user)])
async def search_metiz_by_request(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request
):
    """
    Поиск детали по введенному запросу
    :parameter:
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    search_item = request.query_params.get('main_input')
    res_search = await search_by_request(
        request=search_item,
        session=session,
        model=Metiz
        )
    return templates.TemplateResponse('/finded/metizes.html',
                                      {'request': request,
                                       'metizes': res_search})


@router.get('/{object_id}',
            response_model=None,
            response_model_by_alias=True,
            dependencies=[Depends(check_user)])
async def search_metiz_by_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        object_id: int,
):
    """
    Поиск детали по id
    :parameter:
    session: сессия в асинхронную базу данных
    object_id: id детали
    """
    object_search = await get_object_by_id(
        session=session,
        request_id=object_id,
        model=Metiz
        )
    if object_search:
        return object_search
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'object with {object_id} not found'
        )


@router.delete('/{metiz_id}',
               dependencies=[Depends(check_user)])
async def delete_metiz(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        delete_id: int,
):
    """
    Удаление детали
    :parameter:
    session: сессия в асинхронную базу данных
    delete_id: id детали
    """
    delete_metiz = await get_object_by_id(
        session=session,
        request_id=delete_id,
        model=Metiz
        )
    if not delete_metiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Metiz not found'
            )
    await session.delete(delete_metiz)
    await session.commit()
    return {'message': f'metiz with id={delete_id} was deleted'}


@router.put('/{metiz_id}',
            dependencies=[Depends(check_user)])
async def update_metiz_by_id(
        metiz_updated: MetizUpdatePartial,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        metiz_id: int,
):
    """
    Обновление детали по id
    :parameter:
    metiz_updated: данные для изменения
    session: сессия в асинхронную базу данных
    metiz_id: id детали
    """
    metiz = await get_object_by_id(
        request_id=metiz_id,
        session=session,
        model=Metiz
        )
    return await update_object(
        session=session,
        object_updating=metiz_updated,
        object_for_update=metiz,
    )
