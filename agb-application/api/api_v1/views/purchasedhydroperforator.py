from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.views import check_user
from api.api_v1.crud.hydroperf import hydroperf_crud
from api.api_v1.schemas.purchased_hydroperforator import PurchasedHydroperforatorCreate, \
    PurchasedHydroperforatorUpdatePartial
from core.models import db_helper, PurchasedHydroperforator


templates = Jinja2Templates('templates')

router = APIRouter(
    tags=['PurchasedHydroperforatorBases'],
)


@router.get('/hydroperfs',
            response_model_by_alias=True,
            dependencies=[Depends(check_user)])
async def get_hydroperforators(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request
):
    """
    Вывод всех гидроперфораторов в таблице
    :parameter:
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    hydroperfs = await hydroperf_crud.get_multi(
        session=session
    )
    return templates.TemplateResponse('/search/hydroperfs.html',
                                      {'request': request,
                                       'hydroperfs': hydroperfs})


@router.get('/addnew',
            dependencies=[Depends(check_user)])
async def add_new_hydroperforator(request: Request):
    """
    Вывод формы добавления нового гидроперфоратора
    :parameter:
    request: запрос от пользователя
    """
    return templates.TemplateResponse('/addnew/add_new_hydroperf.html',
                                      {'request': request,
                                       'current_datetime': datetime.now().strftime('%Y-%m-%d %H:%M')})


@router.get('/patch/{item_id}',
            dependencies=[Depends(check_user)])
async def patch_hydroperf_by_id(
    request: Request,
    item_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    """
    Вывод формы редактирования гидроперфоратора по его ID
    :parameter:
    request: запрос от пользователя
    item_id: ID гидроперфоратора
    session: сессия в асинхронную базу данных
    """
    patch_item = await check_hydroperf_exists(
        session=session,
        hydroperf_id=item_id
    )
    print(request.cookies.items())
    return templates.TemplateResponse('/patch/patch_hydroperf.html',
                                      {'request': request,
                                       'current_datetime': datetime.now().strftime('%Y-%m-%d %H:%M"'),
                                       'item': patch_item})


@router.post('/patch',
             response_class=RedirectResponse,
             dependencies=[Depends(check_user)])
async def patch_hydroperforators(
        patch_item: Annotated[PurchasedHydroperforatorUpdatePartial, Form()],
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        ):
    """
    Обновление гидроперфоратора по его ID
    :parameter:
    patch_item: данные для изменения гидроперфоратора
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    object_for_update = await check_hydroperf_exists(
        session=session,
        hydroperf_id=patch_item.id
    )
    await hydroperf_crud.update(
        session=session,
        db_obj=object_for_update,
        obj_in=patch_item
    )
    return RedirectResponse('/hydroperfs/hydroperfs',
                            status_code=status.HTTP_301_MOVED_PERMANENTLY)


@router.post('/create',
             response_model=None,
             response_model_by_alias=True,
             response_class=RedirectResponse,
             dependencies=[Depends(check_user)])
async def create_hydroperforator(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        hydroperf_create: Annotated[PurchasedHydroperforatorCreate, Form()],
        request: Request
        ):
    """
    Создание нового гидроперфоратора
    :parameter:
    session: сессия в асинхронную базу данных
    adapter_create: данные для создания гидроперфоратора
    """
    try:
        await hydroperf_crud.create(
            session=session,
            obj_in=hydroperf_create
        )

        return RedirectResponse('/hydroperfs/hydroperfs',
                                status_code=status.HTTP_301_MOVED_PERMANENTLY)

    except BaseException as ex:
        print(ex)
        return templates.TemplateResponse('/search/hydroperfs.html',
                                          {'request': request,
                                           'message': 'Такая деталь уже существует'})


@router.get('/search',
            dependencies=[Depends(check_user)])
async def search_hydroperforator_by_request(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request
):
    """
    Поиск гидроперфораторов по введенному запросу
    :parameter:
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    search_item = request.query_params.get('main_input')
    res_search = await hydroperf_crud.search(
        request=search_item,
        session=session
        )
    return templates.TemplateResponse('/finded/hydroperfs.html',
                                      {'request': request,
                                       'hydroperfs': res_search})


@router.get('/{object_id}',
            response_model=None,
            response_model_by_alias=True,
            dependencies=[Depends(check_user)])
async def search_hydroperforator_by_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        object_id: int,
):
    """
    Поиск гидроперфоратора по его ID
    :parameter:
    session: сессия в асинхронную базу данных
    object_id: ID гидроперфоратора
    """
    object_search = await check_hydroperf_exists(
        hydroperf_id=object_id,
        session=session
    )
    return object_search


@router.delete('/{hydroperf_id}',
               dependencies=[Depends(check_user)])
async def delete_hydroperforator(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        delete_id: int,
):
    """
    Удаление гидроперфоратора по его ID
    :parameter:
    session: сессия в асинхронную базу данных
    delete_id: ID гидроперфоратора
    """
    delete_hydroperf = await check_hydroperf_exists(
        hydroperf_id=delete_id,
        session=session
    )
    deleted_hydroperf = await hydroperf_crud.remove(
        session=session,
        db_obj=delete_hydroperf
    )
    return deleted_hydroperf


@router.put('/{hydroperf_id}',
            dependencies=[Depends(check_user)])
async def update_hydroperforator_by_id(
        hydroperf_update: PurchasedHydroperforatorUpdatePartial,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        hydroperf_id: int,
):
    """
    Обновление гидроперфоратора по его ID
    :parameter:
    hydroperf_updated: данные для изменения гидроперфоратора
    session: сессия в асинхронную базу данных
    hydroperf_id: ID гидроперфоратора
    """
    hydroperf = await check_hydroperf_exists(
        hydroperf_id=hydroperf_id,
        session=session
    )
    return await hydroperf_crud.update(
        session=session,
        db_obj=hydroperf,
        obj_in=hydroperf_update,
    )


async def check_hydroperf_exists(
    hydroperf_id: int,
    session: AsyncSession
) -> PurchasedHydroperforator:
    """
    Проверка существования детали по id
    :parameter:
    hydroperf_id: id детали
    session: сессия в асинхронную базу данных
    """
    hydroperf = await hydroperf_crud.get(
        hydroperf_id, session
    )
    match hydroperf:
        case None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Не найдено!'
            )
    return hydroperf
