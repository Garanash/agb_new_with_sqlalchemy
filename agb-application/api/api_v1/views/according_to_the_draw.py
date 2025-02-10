from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.views import check_user
from api.api_v1.crud.drawing import drawing_crud
from api.api_v1.schemas.according_to_the_drawing import AccordingToTheDrawCreate, \
    AccordingToTheDrawUpdatePartial

from core.models import db_helper, AccordingToTheDrawing

templates = Jinja2Templates('templates')
router = APIRouter(
    tags=['AccordingToTheDrawBases'],
    dependencies=[Depends(check_user)]
)


@router.get('/drawings',
            response_model_by_alias=True)
async def get_drawings(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request,
        user_data: dict = Depends(check_user)
):
    """
    Вывод всех чертежей в таблице
    :parameter:
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    user_data = check_user()
    print(user_data)
    drawings = await drawing_crud.get_multi(
        session=session
    )
    return templates.TemplateResponse('/search/drawing.html',
                                      {'request': request,
                                       'drawings': drawings})


@router.get('/addnew')
async def add_new_drawing(request: Request,
                          user_data: dict = Depends(check_user)):
    """
    Страница добавления нового чертежа
    :parameter:
    request: запрос от пользователя
    """
    return templates.TemplateResponse('/addnew/add_new_drawing.html',
                                      {'request': request,
                                       'current_datetime': datetime.now().strftime('%Y-%m-%d %H:%M')})


@router.post('/patch',
             response_class=RedirectResponse)
async def patch_drawing(
        patch_item: Annotated[AccordingToTheDrawUpdatePartial, Form()],
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request,
        user_data: dict = Depends(check_user)
        ):
    """
    Обновление информации о конкретном чертеже
    :parameter:
    patch_item: данные для изменения
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    object_for_update = await check_drawing_exists(
        session=session,
        drawing_id=patch_item.id
    )
    await drawing_crud.update(
        session=session,
        obj_in=patch_item,
        db_obj=object_for_update
    )
    return RedirectResponse('/draw/drawings',
                            status_code=status.HTTP_301_MOVED_PERMANENTLY)


@router.get('/search')
async def search_drawing_by_request(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request,
        user_data: dict = Depends(check_user)
):
    """
    Поиск чертежей по введенному запросу
    :parameter:
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    search_item = request.query_params.get('main_input')
    res_search = await drawing_crud.search(
        request=search_item,
        session=session
    )
    return templates.TemplateResponse('/finded/drawing.html',
                                      {'request': request,
                                       'drawings': res_search})


@router.get('/patch/{item_id}')
async def patch_drawing_by_id(request: Request,
                              item_id: int,
                              session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
                              user_data: dict = Depends(check_user)):
    """
    Страница редактирования конкретного чертежа
    :parameter:
    item_id: id чертежа
    session: сессия в асинхронную базу данных
    """
    patch_item = await check_drawing_exists(
        session=session,
        drawing_id=item_id
    )
    return templates.TemplateResponse('/patch/patch_drawing.html',
                                      {'request': request,
                                       'current_datetime': datetime.now().strftime('%Y-%m-%d %H:%M'),
                                       'item': patch_item})


@router.post('/create',
             response_model=None,
             response_model_by_alias=True,
             response_class=RedirectResponse)
async def create_drawing(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        drawing_create: Annotated[AccordingToTheDrawCreate, Form()],
        request: Request,
        user_data: dict = Depends(check_user)
        ):
    """
    Создание нового чертежа
    :parameter:
    session: сессия в асинхронную базу данных
    drawing_create: данные для создания чертежа
    """
    try:
        await drawing_crud.create(
            session=session,
            obj_in=drawing_create
            )
        return RedirectResponse('/draw/drawings',
                                status_code=status.HTTP_301_MOVED_PERMANENTLY)
    except BaseException as ex:
        print(ex)
        return templates.TemplateResponse('/search/drawing.html',
                                          {'request': request,
                                           'message': 'Такая деталь уже существует'})


@router.get('/',
            response_model_by_alias=True)
async def get_according_to_the_draws(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user_data: dict = Depends(check_user)
):
    """
    Вывод всех чертежей в таблице
    :parameter:
    session: сессия в асинхронную базу данных
    """
    according_to_the_draws = await drawing_crud.get_multi(
        session=session
    )
    return according_to_the_draws


@router.post('/new_according_to_the_draw',
             response_model=None,
             response_model_by_alias=True)
async def create_according_to_the_draw(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        according_to_the_draw_create: AccordingToTheDrawCreate,
        user_data: dict = Depends(check_user)
        ):
    """
    Создание нового чертежа
    :parameter:
    session: сессия в асинхронную базу данных
    according_to_the_draw_create: данные для создания чертежа
    :return: созданный чертеж или сообщение об ошибке, если такая деталь уже существует
    """
    according_to_the_draw = await drawing_crud.create(
        session=session,
        obj_in=according_to_the_draw_create
    )
    return according_to_the_draw


@router.get('/{object_id}',
            response_model=None,
            response_model_by_alias=True)
async def search_according_to_the_draw_by_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        object_id: int,
        user_data: dict = Depends(check_user)
):
    """
    Поиск чертежа по id
    :parameter:
    session: сессия в асинхронную базу данных
    object_id: id чертежа
    :return: найденный чертеж или сообщение об ошибке, если чертеж не найден
    """
    object_search = await check_drawing_exists(
        drawing_id=object_id,
        session=session
    )
    return object_search


@router.delete('/{according_to_the_draw_id}')
async def delete_according_to_the_draw(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        delete_id: int,
        user_data: dict = Depends(check_user)
):
    """
    Удаление чертежа по id
    :parameter:
    session: сессия в асинхронную базу данных
    delete_id: id чертежа
    :return: сообщение об успешном удалении или сообщение об ошибке, если чертеж не найден
    :raises HTTPException: если чертеж не найден
    """
    delete_according_to_the_draw = await check_drawing_exists(
        drawing_id=delete_id,
        session=session
    )
    deleted_drawing = await drawing_crud.remove(
        session=session,
        db_obj=delete_according_to_the_draw
    )
    return deleted_drawing


@router.put('/{according_to_the_draw_id}')
async def update_according_to_the_draw_by_id(
        according_to_the_draw_update: AccordingToTheDrawUpdatePartial,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        according_to_the_draw_id: int,
        user_data: dict = Depends(check_user)
):
    """
    Обновление чертежа по id
    :parameter:
    according_to_the_draw_updated: данные для изменения чертежа
    session: сессия в асинхронную базу данных
    according_to_the_draw_id: id чертежа
    :return: измененный чертеж или сообщение об ошибке, если чертеж не найден
    :raises HTTPException: если чертеж не найден
    """
    according_to_the_draw = await check_drawing_exists(
        drawing_id=according_to_the_draw_id,
        session=session
    )
    return await drawing_crud.update(
        session=session,
        db_obj=according_to_the_draw,
        obj_in=according_to_the_draw_update
    )


@router.get('/s/{request_item}')
async def search_according_by_request(
        request_item: str,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user_data: dict = Depends(check_user)
):
    return await drawing_crud.search(
        request=request_item,
        session=session
    )


async def check_drawing_exists(
    drawing_id: int,
    session: AsyncSession
) -> AccordingToTheDrawing:
    """
    Проверка существования детали по id
    :parameter:
    drawing_id: id детали
    session: сессия в асинхронную базу данных
    """
    drawing = await drawing_crud.get(
        drawing_id, session
    )
    match drawing:
        case None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Не найдено!'
            )
    return drawing
