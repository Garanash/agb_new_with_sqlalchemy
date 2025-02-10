from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.views import check_user
from api.api_v1.crud.metiz import metiz_crud
from api.api_v1.schemas.metizes import MetizCreate, MetizUpdatePartial
from core.models import db_helper, Metiz

templates = Jinja2Templates('templates')

router = APIRouter(
    tags=['MetizBases'],
    dependencies=[Depends(check_user)]
)


@router.get('/metizes',
            response_model_by_alias=True)
async def get_metizes(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request,
        user_data: dict = Depends(check_user)
):
    """
    Вывод всех метизов в таблице
    :parameter:
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    metiz = await metiz_crud.get_multi(
        session=session
    )
    return templates.TemplateResponse('/search/metizes.html',
                                      {'request': request,
                                       'metizes': metiz})


@router.get('/addnew')
async def add_new_metiz(request: Request,
                        user_data: dict = Depends(check_user)):
    """
    Добавление нового метиза
    :parameter:
    request: запрос от пользователя
    """
    return templates.TemplateResponse('/addnew/add_new_metiz.html',
                                      {'request': request,
                                       'current_datetime': datetime.now().strftime('%Y-%m-%d %H:%M')})


@router.get("/patch/{item_id}")
async def patch_metiz_by_id(request: Request,
                            item_id: int,
                            session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
                            user_data: dict = Depends(check_user)):
    patch_item = await check_metiz_exists(
        session=session,
        metiz_id=item_id
    )
    return templates.TemplateResponse('/patch/patch_metiz.html',
                                      {'request': request,
                                       'current_datetime': datetime.now().strftime("%Y-%m-%d %H:%M"),
                                       'item': patch_item})


@router.post('/patch',
             response_class=RedirectResponse)
async def patch_metizes(
        patch_item: Annotated[MetizUpdatePartial, Form()],
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user_data: dict = Depends(check_user)
        ):
    """
    Обновление детали
    :parameter:
    patch_item: данные для изменения
    session: сессия в асинхронную базу данных
    """
    object_for_update = await check_metiz_exists(
        session=session,
        metiz_id=patch_item.id
    )
    await metiz_crud.update(
        session=session,
        db_obj=object_for_update,
        obj_in=patch_item
    )
    return RedirectResponse('/metiz/metizes',
                            status_code=status.HTTP_301_MOVED_PERMANENTLY)


@router.post("/create",
             response_model=None,
             response_model_by_alias=True,
             response_class=RedirectResponse)
async def create_metiz(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        metiz_create: Annotated[MetizCreate, Form()],
        request: Request,
        user_data: dict = Depends(check_user)):
    """
    Создание новой детали
    :parameter:
    session: сессия в асинхронную базу данных
    metiz_create: данные для создания
    request: запрос от пользователя
    """
    try:
        await metiz_crud.create(
            session=session,
            obj_in=metiz_create
        )
        return RedirectResponse('/metiz/metizes',
                                status_code=status.HTTP_301_MOVED_PERMANENTLY)

    except BaseException:
        return templates.TemplateResponse('/search/metizes.html',
                                          {'request': request,
                                           "message": 'Такая деталь уже существует'})


@router.get('/search')
async def search_metiz_by_request(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request,
        user_data: dict = Depends(check_user)
):
    """
    Поиск детали по введенному запросу
    :parameter:
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    search_item = request.query_params.get('main_input')
    res_search = await metiz_crud.search(
        request=search_item,
        session=session
        )
    return templates.TemplateResponse('/finded/metizes.html',
                                      {'request': request,
                                       'metizes': res_search})


@router.get('/{object_id}',
            response_model=None,
            response_model_by_alias=True)
async def search_metiz_by_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        object_id: int,
        user_data: dict = Depends(check_user)
):
    """
    Поиск детали по id
    :parameter:
    session: сессия в асинхронную базу данных
    object_id: id детали
    """
    object_search = await check_metiz_exists(
        session=session,
        metiz_id=object_id
    )
    return object_search


@router.delete('/{metiz_id}')
async def delete_metiz(
        delete_id: int,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user_data: dict = Depends(check_user)
):
    """
    Удаление детали
    :parameter:
    session: сессия в асинхронную базу данных
    delete_id: id детали
    """
    metiz = await check_metiz_exists(
        session=session,
        metiz_id=delete_id
    )
    metiz_deleted = await metiz_crud.remove(metiz, session)
    return metiz_deleted


@router.put('/{metiz_id}')
async def update_metiz_by_id(
        metiz_updated: MetizUpdatePartial,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        metiz_id: int,
        user_data: dict = Depends(check_user)
):
    """
    Обновление детали по id
    :parameter:
    metiz_updated: данные для изменения
    session: сессия в асинхронную базу данных
    metiz_id: id детали
    """
    metiz = await check_metiz_exists(
        session=session,
        metiz_id=metiz_id
    )
    metiz_updated = await metiz_crud.update(
        session=session,
        db_obj=metiz,
        obj_in=metiz_updated
        )
    return metiz_updated


async def check_metiz_exists(
    metiz_id: int,
    session: AsyncSession
) -> Metiz:
    """
    Проверка существования детали по id
    :parameter:
    metiz_id: id детали
    session: сессия в асинхронную базу данных
    """
    metiz = await metiz_crud.get(
        metiz_id, session
    )
    match metiz:
        case None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Метиз не найден!'
            )
    return metiz
