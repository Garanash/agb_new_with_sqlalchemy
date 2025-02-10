from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.views import check_user
from api.api_v1.crud.RWD import rwd_crud
from api.api_v1.schemas.RWD import RWDCreate, RWDUpdatePartial
from core.models import db_helper, RWD


templates = Jinja2Templates('templates')
router = APIRouter(
    tags=['RWDBases'],
    dependencies=[Depends(check_user)]
)


@router.get('/RWDs',
            response_model_by_alias=True)
async def get_rwd(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request,
        user_data: dict = Depends(check_user)
):
    """
    Вывод всех РВД в таблице
    :parameter:
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    rwd = await rwd_crud.get_multi(
        session=session
    )
    return templates.TemplateResponse('/search/rwd.html',
                                      {'request': request,
                                       'rwd': rwd})


@router.get('/',
            response_model_by_alias=True)
async def get_rwd_item(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user_data: dict = Depends(check_user)
):
    """
    Вывод одного РВД по его id
    :parameter:
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    rwd_item = await rwd_crud.get_multi(
        session=session
    )
    return rwd_item


@router.get('/addnew')
async def add_new_rwd(request: Request,
                      user_data: dict = Depends(check_user)):
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
                          session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
                          user_data: dict = Depends(check_user)):
    """
    Редактирование РВД по его id
    :parameter:
    request: запрос от пользователя
    item_id: id РВД для редактирования
    """
    patch_item = await check_rwd_exists(
        session=session,
        rwd_id=item_id
    )
    return templates.TemplateResponse('/patch/patch_rwd.html',
                                      {'request': request,
                                       'current_datetime': datetime.now().strftime('%Y-%m-%d %H:%M'),
                                       'item': patch_item})


@router.post('/patch',
             response_class=RedirectResponse)
async def patch_rwd(
        patch_item: Annotated[RWDUpdatePartial, Form()],
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request,
        user_data: dict = Depends(check_user)
        ):
    """
    Редактирование РВД по его id
    :parameter:
    patch_item: данные для редактирования
    session: сессия в асинхронную базу данных
    """
    object_for_update = await check_rwd_exists(
        session=session,
        rwd_id=patch_item.id
    )
    await rwd_crud.update(
        session=session,
        db_obj=object_for_update,
        obj_in=patch_item
    )
    return RedirectResponse('/RWD/RWDs',
                            status_code=status.HTTP_301_MOVED_PERMANENTLY)


@router.post('/create',
             response_model=None,
             response_model_by_alias=True,
             response_class=RedirectResponse)
async def create_rwd(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        rwd_create: Annotated[RWDCreate, Form()],
        request: Request,
        user_data: dict = Depends(check_user)
        ):
    """
    создание нового РВД
    :parameter:
    rwd_create: данные для создания
    session: сессия в асинхронную базу данных
    """
    try:
        await rwd_crud.create(
            session=session,
            obj_in=rwd_create
            )
        return RedirectResponse('/RWD/RWDs',
                                status_code=status.HTTP_301_MOVED_PERMANENTLY)

    except BaseException:
        return templates.TemplateResponse('/search/rwd.html',
                                          {'request': request,
                                           'message': 'Такая деталь уже существует'})


@router.get('/search')
async def search_rwd_by_request(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request,
        user_data: dict = Depends(check_user)
):
    """
    Поиск РВД по детальному ключу
    :parameter:
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    search_item = request.query_params.get('main_input')
    res_search = await rwd_crud.search(
        request=search_item,
        session=session
        )
    return templates.TemplateResponse('/finded/rwds.html',
                                      {'request': request,
                                       'rwds': res_search})


@router.get('/{rwd_item_id}',
            response_model=None,
            response_model_by_alias=True)
async def search_rwd_item_by_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        rwd_item_id: int,
        user_data: dict = Depends(check_user)
):
    """
    Поиск РВД по его id
    :parameter:
    session: сессия в асинхронную базу данных
    rwd_item_id: id РВД для поиска
    """
    object_search = await check_rwd_exists(
        rwd_id=rwd_item_id,
        session=session
    )
    return object_search


@router.delete('/{rwd_item_id}')
async def delete_rwd_item(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        delete_id: int,
        user_data: dict = Depends(check_user)
):
    """
    Удаление РВД по его id
    :parameter:
    session: сессия в асинхронную базу данных
    delete_id: id РВД для удаления
    """
    delete_rwd_item = await check_rwd_exists(
        rwd_id=delete_id,
        session=session)

    deleted_rwd = await rwd_crud.remove(
        session=session,
        db_obj=delete_rwd_item
    )
    return deleted_rwd


@router.put('/{rwd_item_id}')
async def update_rwd_item_by_id(
        rwd_item_update: RWDUpdatePartial,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        rwd_item_id: int,
        user_data: dict = Depends(check_user)
):
    """
    Редактирование РВД по его id
    :parameter:
    rwd_item_update: данные для редактирования
    session: сессия в асинхронную базу данных
    rwd_item_id: id РВД для редактирования
    """
    rwd_item = await check_rwd_exists(rwd_item_id, session)
    return await rwd_crud.update(
        session=session,
        db_obj=rwd_item,
        obj_in=rwd_item_update
    )


# @router.get('/s/{request_item}')
# async def search_rwd_by_request(
#         request_item: str,
#         session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
# ):
#     return await search_by_request(request=request_item, session=session, model=RWD)


async def check_rwd_exists(
    rwd_id: int,
    session: AsyncSession
) -> RWD:
    """
    Проверка существования детали по id
    :parameter:
    rwd_id: id детали
    session: сессия в асинхронную базу данных
    """
    rwd = await rwd_crud.get(
        rwd_id, session
    )
    match rwd:
        case None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Не найдено!'
            )
    return rwd
