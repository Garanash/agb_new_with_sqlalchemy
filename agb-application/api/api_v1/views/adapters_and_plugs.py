from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.views import check_user
from api.api_v1.crud.adapter import adapter_crud
from api.api_v1.schemas.adapters_and_plugs import (AdapterAndPlugsCreate,
                                                   AdapterAndPlugsUpdatePartial)
from core.models import db_helper, AdaptersAndPlugs


templates = Jinja2Templates('templates')

router = APIRouter(
    tags=['AdapterAndPlugsBases'],
    dependencies=[Depends(check_user)]
)


@router.get('/adapters',
            response_model_by_alias=True)
async def get_adapters_and_plugss(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request,
        user_data: dict = Depends(check_user)
):
    """
    Вывод всех адаптеров и разъемов в таблице
    :parameter:
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    print(user_data)
    adapters_and_plugs = await adapter_crud.get_multi(
        session=session
    )
    return templates.TemplateResponse('/search/adapters.html',
                                      {'request': request,
                                       'adapters': adapters_and_plugs,
                                       "userdata": user_data,
                                       'tag': 'adapters'})


@router.get('/addnew')
async def add_new_adapter(request: Request,
                          user_data: dict = Depends(check_user)):
    """
    Добавление нового адаптера и разъема
    :parameter:
    request: запрос от пользователя
    """
    return templates.TemplateResponse('/addnew/add_new_adapter.html',
                                      {'request': request,
                                       'current_datetime': datetime.now().strftime('%Y-%m-%d %H:%M'),
                                       "userdata": user_data,
                                       'tag': 'adapters'})


@router.get('/patch/{item_id}')
async def patch_adapter_by_id(
        request: Request,
        item_id: int,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user_data: dict = Depends(check_user)
):
    """
    Изменение адаптера и разъема по его id
    :parameter:
    request: запрос от пользователя
    item_id: id изменяемого адаптера и разъема
    session: сессия в асинхронную базу данных
    """
    patch_item = await check_adapter_exists(
        session=session,
        adapter_id=item_id
    )
    return templates.TemplateResponse('/patch/patch_adapters.html',
                                      {'request': request,
                                       'current_datetime': datetime.now().strftime('%Y-%m-%d %H:%M'),
                                       'item': patch_item,
                                       "userdata": user_data,
                                       'tag': 'adapters'})


@router.post('/patch',
             response_class=RedirectResponse)
async def patch_adapters(
        patch_item: Annotated[AdapterAndPlugsUpdatePartial, Form()],
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user_data: dict = Depends(check_user)
):
    """
    Изменение адаптера и разъема по его id
    :parameter:
    patch_item: данные для изменения
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    object_for_update = await check_adapter_exists(
        session=session,
        adapter_id=patch_item.id
    )
    await adapter_crud.update(
        session=session,
        db_obj=object_for_update,
        obj_in=patch_item
    )
    return RedirectResponse("/adapters/adapters",
                            status_code=status.HTTP_301_MOVED_PERMANENTLY)


@router.post('/create',
             response_model=None,
             response_model_by_alias=True,
             response_class=RedirectResponse)
async def create_adapter(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        adapter_create: Annotated[AdapterAndPlugsCreate, Form()],
        request: Request,
        user_data: dict = Depends(check_user)
):
    """
    Создание нового адаптера и разъема
    :parameter:
    session: сессия в асинхронную базу данных
    adapter_create: данные для создания
    request: запрос от пользователя
    """
    try:
        await adapter_crud.create(
            session=session,
            obj_in=adapter_create,
            )
        return RedirectResponse('/adapters/adapters',
                                status_code=status.HTTP_301_MOVED_PERMANENTLY)

    except BaseException:
        return templates.TemplateResponse('/search/adapters.html',
                                          {'request': request,
                                           'message': 'Такая деталь уже существует',
                                           "userdata": user_data,
                                           'tag': 'adapters'})


@router.get('/search')
async def search_adapter_by_request(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request,
        user_data: dict = Depends(check_user)
):
    """
    Поиск адаптера и разъема по введенному запросу
    :parameter:
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    search_item = request.query_params.get('main_input')
    res_search = await adapter_crud.search(
        request=search_item,
        session=session
        )
    return templates.TemplateResponse('/finded/adapters.html',
                                      {'request': request,
                                       'adapters': res_search,
                                       "userdata": user_data,
                                       'tag': 'adapters'})


@router.get('/{object_id}',
            response_model=None,
            response_model_by_alias=True)
async def search_adapter_by_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        object_id: int,
        user_data: dict = Depends(check_user)
):
    """
    Поиск адаптера и разъема по его id
    :parameter:
    session: сессия в асинхронную базу данных
    object_id: id адаптера и разъема
    :return: найденный адаптер и разъем или ошибка 404 если не найден
    """
    adapter = await check_adapter_exists(
        session=session,
        adapter_id=object_id,
    )
    return adapter


@router.delete('/{adapter_id}')
async def delete_adapter(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        delete_id: int,
        user_data: dict = Depends(check_user)
):
    """
    Удаление адаптера и разъема по его id
    :parameter:
    session: сессия в асинхронную базу данных
    delete_id: id удаляемого адаптера и разъема
    :return: сообщение об успешном удалении адаптера и разъема или ошибка 404 если адаптер не найден  # noqa: E501
    """
    delete_adapter = await check_adapter_exists(
        adapter_id=delete_id,
        session=session,
    )
    return delete_adapter


@router.put('/{adapter_id}')
async def update_adapter_by_id(
        adapter_update: AdapterAndPlugsUpdatePartial,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        adapter_id: int,
        user_data: dict = Depends(check_user)
):
    """
    Обновление адаптера и разъема по его id
    :parameter:
    adapter_updated: данные для изменения
    session: сессия в асинхронную базу данных
    adapter_id: id адаптера и разъема
    :return: сообщение об успешном изменении адаптера и разъема или ошибка 404 если адаптер не найден  # noqa: E501
    """
    adapter = await check_adapter_exists(
        adapter_id=adapter_id,
        session=session
    )
    return await adapter_crud.update(
        session=session,
        db_obj=adapter,
        obj_in=adapter_update,
    )


async def check_adapter_exists(
    adapter_id: int,
    session: AsyncSession
) -> AdaptersAndPlugs:
    """
    Проверка существования детали по id
    :parameter:
    adapter_id: id детали
    session: сессия в асинхронную базу данных
    """
    adapter = await adapter_crud.get(
        adapter_id, session
    )
    match adapter:
        case None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Не найдено!'
            )
    return adapter
