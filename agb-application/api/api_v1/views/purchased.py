from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.views import check_user
from api.api_v1.schemas.purchased import PurchasedRead, PurchasedCreate, PurchasedUpdatePartial, PurchasedBase, PurchasedDelete
from core.models import db_helper, Purchased
from api.api_v1.crud.CRUD import get_all_objects, create_new_object, update_object, get_object_by_id, delete_object, \
    search_by_request

templates = Jinja2Templates('templates')

router = APIRouter(
    tags=['PurchasedBases'],
)


@router.get('/purchased',
            response_model_by_alias=True,
            dependencies=[Depends(check_user)])
async def get_purchases(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request
):
    """
    Вывод всех покупной позиции в таблице
    :parameter:
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    purchases = await get_all_objects(
        session=session,
        model=Purchased
        )
    return templates.TemplateResponse('/search/purchased.html',
                                      {'request': request,
                                       'purchased': purchases})


@router.get('/addnew',
            dependencies=[Depends(check_user)])
async def add_new_purchase(request: Request):
    """
    Вывод страницы добавления новой покупной позиции
    :parameter:
    request: запрос от пользователя
    """
    return templates.TemplateResponse('/addnew/add_new_purchase.html',
                                      {'request': request,
                                       'current_datetime': datetime.now().strftime('%Y-%m-%d %H:%M')})


@router.get('/patch/{item_id}',
            dependencies=[Depends(check_user)])
async def patch_purchase_by_id(
    request: Request,
    item_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    """
    Вывод страницы изменения покупной позиции
    :parameter:
    request: запрос от пользователя
    item_id: идентификатор покупной позиции
    """
    patch_item = await get_object_by_id(
        session=session,
        model=Purchased,
        request_id=item_id
        )
    print(request.cookies.items())
    return templates.TemplateResponse('/patch/patch_purchase.html',
                                      {'request': request,
                                       'current_datetime': datetime.now().strftime('%Y-%m-%d %H:%M'),
                                       'item': patch_item})


@router.post('/patch',
             response_class=RedirectResponse,
             dependencies=[Depends(check_user)])
async def patch_purchases(
        patch_item: Annotated[PurchasedUpdatePartial, Form()],
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request
        ):
    """
    Изменение покупной позиции
    :parameter:
    patch_item: данные изменения покупной позиции
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    object_for_update = await get_object_by_id(
        request_id=patch_item.id,
        session=session,
        model=Purchased
        )
    await update_object(
        session=session,
        object_for_update=object_for_update,
        object_updating=patch_item,
        partial=True
        )
    return RedirectResponse('/purchased/purchased',
                            status_code=status.HTTP_301_MOVED_PERMANENTLY)


@router.post('/create',
             response_model=None,
             response_model_by_alias=True,
             response_class=RedirectResponse,
             dependencies=[Depends(check_user)])
async def create_purchase(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        purchase_create: Annotated[PurchasedCreate, Form()],
        request: Request
        ):
    """
    Создание новой покупной позиции
    :parameter:
    purchase_create: данные новой покупной позиции
    session: сессия в асинхронную базу данных
    """
    try:
        purchase = await create_new_object(
            session=session,
            object_create=purchase_create,
            model=Purchased
            )
        return RedirectResponse('/purchased/purchased',
                                status_code=status.HTTP_301_MOVED_PERMANENTLY)

    except BaseException:
        return templates.TemplateResponse('/search/purchased.html',
                                          {'request': request,
                                           'message': 'Такая деталь уже существует'})


@router.get('/search',
            dependencies=[Depends(check_user)])
async def search_purchase_by_request(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request
):
    """
    Поиск покупной позиции по определенному критерию
    :parameter:
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    search_item = request.query_params.get('main_input')
    res_search = await search_by_request(
        request=search_item,
        session=session,
        model=Purchased
        )
    return templates.TemplateResponse('/finded/purchased.html',
                                      {'request': request,
                                       'purchased': res_search})


@router.get('/{object_id}',
            response_model=None,
            response_model_by_alias=True,
            dependencies=[Depends(check_user)])
async def search_purchase_by_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        object_id: int,
):
    """
    Поиск покупной позиции по её идентификатору
    :parameter:
    session: сессия в асинхронную базу данных
    object_id: идентификатор покупной позиции
    """
    object_search = await get_object_by_id(
        session=session,
        request_id=object_id,
        model=Purchased
        )
    if object_search:
        return object_search
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'object with {object_id} not found'
        )


@router.delete('/{purchase_id}',
               dependencies=[Depends(check_user)])
async def delete_purchase(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        delete_id: int,
):
    """
    Удаление покупной позиции по её идентификатору
    :parameter:
    session: сессия в асинхронную базу данных
    delete_id: идентификатор покупной позиции
    """
    delete_purchase = await get_object_by_id(
        session=session,
        request_id=delete_id,
        model=Purchased
        )
    if not delete_purchase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Purchase not found'
            )
    await session.delete(delete_purchase)
    await session.commit()
    return {'message': f'Purchase with id={delete_id} was deleted'}


@router.put('/{purchase_id}',
            dependencies=[Depends(check_user)])
async def update_purchase_by_id(
        purchase_updated: PurchasedUpdatePartial,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        metiz_id: int,
):
    """
    Обновление покупной позиции по её идентификатору
    :parameter:
    purchase_updated: данные для обновления покупной позиции
    session: сессия в асинхронную базу данных
    metiz_id: идентификатор покупной позиции
    """
    purchase = await get_object_by_id(
        request_id=metiz_id,
        session=session,
        model=Purchased
        )
    return await update_object(
        session=session,
        object_updating=purchase_updated,
        object_for_update=purchase,
    )
