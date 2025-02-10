from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.views import check_user
from api.api_v1.crud.purchased import purchased_crud
from api.api_v1.schemas.purchased import (PurchasedCreate,
                                          PurchasedUpdatePartial)
from core.models import db_helper, Purchased


templates = Jinja2Templates('templates')

router = APIRouter(
    tags=['PurchasedBases'],
    dependencies=[Depends(check_user)]
)


@router.get('/purchased',
            response_model_by_alias=True)
async def get_purchases(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request,
        user_data: dict = Depends(check_user)
):
    """
    Вывод всех покупной позиции в таблице
    :parameter:
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    purchases = await purchased_crud.get_multi(
        session=session
    )
    return templates.TemplateResponse('/search/purchased.html',
                                      {'request': request,
                                       'purchased': purchases})


@router.get('/addnew')
async def add_new_purchase(request: Request,
                           user_data: dict = Depends(check_user)):
    """
    Вывод страницы добавления новой покупной позиции
    :parameter:
    request: запрос от пользователя
    """
    return templates.TemplateResponse('/addnew/add_new_purchase.html',
                                      {'request': request,
                                       'current_datetime': datetime.now().strftime('%Y-%m-%d %H:%M')})


@router.get('/patch/{item_id}')
async def patch_purchase_by_id(
    request: Request,
    item_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_data: dict = Depends(check_user)
):
    """
    Вывод страницы изменения покупной позиции
    :parameter:
    request: запрос от пользователя
    item_id: идентификатор покупной позиции
    """
    patch_item = await check_purchase_exists(
        purchase_id=item_id,
        session=session
    )
    print(request.cookies.items())
    return templates.TemplateResponse('/patch/patch_purchase.html',
                                      {'request': request,
                                       'current_datetime': datetime.now().strftime('%Y-%m-%d %H:%M'),
                                       'item': patch_item})


@router.post('/patch',
             response_class=RedirectResponse)
async def patch_purchases(
        patch_item: Annotated[PurchasedUpdatePartial, Form()],
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request,
        user_data: dict = Depends(check_user)
        ):
    """
    Изменение покупной позиции
    :parameter:
    patch_item: данные изменения покупной позиции
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    object_for_update = await check_purchase_exists(
        purchase_id=patch_item.id,
        session=session
    )

    await purchased_crud.update(
        session=session,
        db_obj=object_for_update,
        obj_in=patch_item
    )
    return RedirectResponse('/purchased/purchased',
                            status_code=status.HTTP_301_MOVED_PERMANENTLY)


@router.post('/create',
             response_model=None,
             response_model_by_alias=True,
             response_class=RedirectResponse)
async def create_purchase(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        purchase_create: Annotated[PurchasedCreate, Form()],
        request: Request,
        user_data: dict = Depends(check_user)
        ):
    """
    Создание новой покупной позиции
    :parameter:
    purchase_create: данные новой покупной позиции
    session: сессия в асинхронную базу данных
    """
    try:
        await purchased_crud.create(
            session=session,
            obj_in=purchase_create
        )
        return RedirectResponse('/purchased/purchased',
                                status_code=status.HTTP_301_MOVED_PERMANENTLY)

    except BaseException:
        return templates.TemplateResponse('/search/purchased.html',
                                          {'request': request,
                                           'message': 'Такая деталь уже существует'})


@router.get('/search')
async def search_purchase_by_request(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request,
        user_data: dict = Depends(check_user)
):
    """
    Поиск покупной позиции по определенному критерию
    :parameter:
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    search_item = request.query_params.get('main_input')
    res_search = await purchased_crud.search(
        request=search_item,
        session=session
        )
    return templates.TemplateResponse('/finded/purchased.html',
                                      {'request': request,
                                       'purchased': res_search})


@router.get('/{object_id}',
            response_model=None,
            response_model_by_alias=True)
async def search_purchase_by_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        object_id: int,
        user_data: dict = Depends(check_user)
):
    """
    Поиск покупной позиции по её идентификатору
    :parameter:
    session: сессия в асинхронную базу данных
    object_id: идентификатор покупной позиции
    """
    purchase = await check_purchase_exists(
        purchase_id=object_id,
        session=session
    )
    return purchase


@router.delete('/{purchase_id}')
async def delete_purchase(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        delete_id: int,
        user_data: dict = Depends(check_user)
):
    """
    Удаление покупной позиции по её идентификатору
    :parameter:
    session: сессия в асинхронную базу данных
    delete_id: идентификатор покупной позиции
    """
    purchase = await check_purchase_exists(
        purchase_id=delete_id,
        session=session
    )
    delete_purchase = await purchased_crud.remove(
        db_obj=purchase,
        session=session
    )
    return delete_purchase


@router.put('/{purchase_id}')
async def update_purchase_by_id(
        purchase_update: PurchasedUpdatePartial,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        purchase_id: int,
        user_data: dict = Depends(check_user)
):
    """
    Обновление покупной позиции по её идентификатору
    :parameter:
    purchase_updated: данные для обновления покупной позиции
    session: сессия в асинхронную базу данных
    metiz_id: идентификатор покупной позиции
    """
    purchase = await check_purchase_exists(
        purchase_id=purchase_id,
        session=session
    )
    return await purchased_crud.update(
        session=session,
        db_obj=purchase,
        obj_in=purchase_update
    )


async def check_purchase_exists(
    purchase_id: int,
    session: AsyncSession
) -> Purchased:
    """
    Проверка существования детали по id
    :parameter:
    purchase_id: id детали
    session: сессия в асинхронную базу данных
    """
    purchased = await purchased_crud.get(
        purchase_id, session
    )
    match purchased:
        case None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Не найдено!'
            )
    return purchased
