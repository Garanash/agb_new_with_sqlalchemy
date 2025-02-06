from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.views import check_user
from api.api_v1.schemas.adapters_and_plugs import AdapterAndPlugsRead, AdapterAndPlugsCreate, \
    AdapterAndPlugsUpdatePartial, AdapterAndPlugsBase, AdapterAndPlugsDelete
from core.models import db_helper, AdaptersAndPlugs
from api.api_v1.crud.CRUD import get_all_objects, create_new_object, update_object, get_object_by_id, delete_object, \
    search_by_request

templates = Jinja2Templates('templates')

router = APIRouter(
    tags=['AdapterAndPlugsBases'],
)


@router.get('/adapters',
            response_model_by_alias=True,
            dependencies=[Depends(check_user)])
async def get_adapters_and_plugss(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request
):
    """
    Вывод всех адаптеров и разъемов в таблице
    :parameter:
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    adapters_and_plugs = await get_all_objects(
        session=session,
        model=AdaptersAndPlugs
        )
    return templates.TemplateResponse('/search/adapters.html',
                                      {'request': request,
                                       'adapters': adapters_and_plugs})


@router.get('/addnew',
            dependencies=[Depends(check_user)])
async def add_new_adapter(request: Request):
    """
    Добавление нового адаптера и разъема
    :parameter:
    request: запрос от пользователя
    """
    return templates.TemplateResponse('/addnew/add_new_adapter.html',
                                      {'request': request,
                                       'current_datetime': datetime.now().strftime('%Y-%m-%d %H:%M')})


@router.get('/patch/{item_id}',
            dependencies=[Depends(check_user)])
async def patch_adapter_by_id(
        request: Request,
        item_id: int,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    """
    Изменение адаптера и разъема по его id
    :parameter:
    request: запрос от пользователя
    item_id: id изменяемого адаптера и разъема
    session: сессия в асинхронную базу данных
    """
    patch_item = await get_object_by_id(
        session=session,
        model=AdaptersAndPlugs,
        request_id=item_id
        )
    return templates.TemplateResponse('/patch/patch_adapters.html',
                                      {'request': request,
                                       'current_datetime': datetime.now().strftime('%Y-%m-%d %H:%M'),
                                       'item': patch_item})


@router.post('/patch',
             response_class=RedirectResponse,
             dependencies=[Depends(check_user)])
async def patch_adapters(
        patch_item: Annotated[AdapterAndPlugsUpdatePartial, Form()],
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request
):
    """
    Изменение адаптера и разъема по его id
    :parameter:
    patch_item: данные для изменения
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    object_for_update = await get_object_by_id(
        request_id=patch_item.id,
        session=session,
        model=AdaptersAndPlugs
        )
    await update_object(
        session=session,
        object_for_update=object_for_update,
        object_updating=patch_item,
        partial=True
        )
    return RedirectResponse("/adapters/adapters",
                            status_code=status.HTTP_301_MOVED_PERMANENTLY)


@router.post('/create',
             response_model=None,
             response_model_by_alias=True,
             response_class=RedirectResponse,
             dependencies=[Depends(check_user)])
async def create_adapter(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        adapter_create: Annotated[AdapterAndPlugsCreate, Form()],
        request: Request
):
    """
    Создание нового адаптера и разъема
    :parameter:
    session: сессия в асинхронную базу данных
    adapter_create: данные для создания
    request: запрос от пользователя
    """
    try:
        adapter = await create_new_object(
            session=session,
            object_create=adapter_create,
            model=AdaptersAndPlugs
            )
        return RedirectResponse('/adapters/adapters',
                                status_code=status.HTTP_301_MOVED_PERMANENTLY)

    except BaseException:
        return templates.TemplateResponse('/search/adapters.html',
                                          {'request': request,
                                           'message': 'Такая деталь уже существует'})


@router.get('/search',
            dependencies=[Depends(check_user)])
async def search_adapter_by_request(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request
):
    """
    Поиск адаптера и разъема по введенному запросу
    :parameter:
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    search_item = request.query_params.get('main_input')
    res_search = await search_by_request(
        request=search_item,
        session=session,
        model=AdaptersAndPlugs
        )
    return templates.TemplateResponse('/finded/adapters.html',
                                      {'request': request,
                                       'adapters': res_search})


@router.get('/{object_id}',
            response_model=None,
            response_model_by_alias=True,
            dependencies=[Depends(check_user)])
async def search_adapter_by_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        object_id: int,
):
    """
    Поиск адаптера и разъема по его id
    :parameter:
    session: сессия в асинхронную базу данных
    object_id: id адаптера и разъема
    :return: найденный адаптер и разъем или ошибка 404 если не найден
    """
    object_search = await get_object_by_id(
        session=session,
        request_id=object_id,
        model=AdaptersAndPlugs
        )
    if object_search:
        return object_search
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'object with {object_id} not found'
        )


@router.delete('/{adapter_id}',
               dependencies=[Depends(check_user)])
async def delete_adapter(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        delete_id: int,
):
    """
    Удаление адаптера и разъема по его id
    :parameter:
    session: сессия в асинхронную базу данных
    delete_id: id удаляемого адаптера и разъема
    :return: сообщение об успешном удалении адаптера и разъема или ошибка 404 если адаптер не найден  # noqa: E501
    """
    delete_adapter = await get_object_by_id(
        session=session,
        request_id=delete_id,
        model=AdaptersAndPlugs
        )
    if not delete_adapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='adapter not found'
            )
    await session.delete(delete_adapter)
    await session.commit()
    return {'message': f'Adapter with id={delete_id} was deleted'}


@router.put('/{adapter_id}',
            dependencies=[Depends(check_user)])
async def update_adapter_by_id(
        adapter_updated: AdapterAndPlugsUpdatePartial,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        adapter_id: int,
):
    """
    Обновление адаптера и разъема по его id
    :parameter:
    adapter_updated: данные для изменения
    session: сессия в асинхронную базу данных
    adapter_id: id адаптера и разъема
    :return: сообщение об успешном изменении адаптера и разъема или ошибка 404 если адаптер не найден
    """
    adapter = await get_object_by_id(
        request_id=adapter_id,
        session=session,
        model=AdaptersAndPlugs
        )
    return await update_object(
        session=session,
        object_updating=adapter_updated,
        object_for_update=adapter,
    )
