from typing import Annotated
from datetime import datetime
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request
from watchfiles import awatch
from fastapi.responses import RedirectResponse, PlainTextResponse
from api.api_v1.schemas.metizes import MetizRead, MetizCreate, MetizUpdatePartial, MetizBase, MetizDelete, MetizUpdate
from core.models import db_helper, Metiz
from api.api_v1.crud.CRUD import get_all_objects, create_new_object, update_object, get_object_by_id, delete_object, \
    search_by_request

templates = Jinja2Templates('templates')

router = APIRouter(
    tags=['MetizBases'],
)


@router.get('/metizes', response_model_by_alias=True)
async def get_metizes(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request
):
    """
    вывод всех метизов в таблице
    :parameter:
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    metiz = await get_all_objects(session=session, model=Metiz)
    return templates.TemplateResponse('/search/metizes.html', {"request": request, "metizes": metiz})


@router.get("/addnew")
async def add_new_metiz(request: Request):
    return templates.TemplateResponse("/addnew/add_new_metiz.html",
                                      {"request": request,
                                       "current_datetime": datetime.now().strftime("%Y-%m-%dT%H:%M")})


@router.get("/patch/{item_id}")
async def patch_metiz_by_id(request: Request, item_id: int,
                            session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    patch_item = await get_object_by_id(session=session, model=Metiz, request_id=item_id)

    return templates.TemplateResponse("/patch/patch_metiz.html",
                                      {"request": request,
                                       "current_datetime": datetime.now().strftime("%Y-%m-%dT%H:%M"),
                                       "item": patch_item})


@router.post("/patch", response_class=RedirectResponse)
async def patch_metizes(
        patch_item: Annotated[MetizUpdatePartial, Form()],
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request):
    object_for_update = await get_object_by_id(request_id=patch_item.id, session=session, model=Metiz)
    await update_object(session=session, object_for_update=object_for_update, object_updating=patch_item, partial=True)
    return RedirectResponse("/metiz/metizes", status_code=301)


@router.post("/create", response_model=None, response_model_by_alias=True, response_class=RedirectResponse)
async def create_metiz(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        metiz_create: Annotated[MetizCreate, Form()],
        request: Request):
    try:
        metiz = await create_new_object(session=session, object_create=metiz_create, model=Metiz)
        return RedirectResponse("/metiz/metizes", status_code=301)

    except BaseException:
        return templates.TemplateResponse("/search/metizes.html",
                                          {'request': request, "message": "Такая деталь уже существует"})
        # return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="metiz already exists")


@router.get('/search')
async def search_metiz_by_request(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request
):
    search_item = request.query_params.get('main_input')
    res_search = await search_by_request(request=search_item, session=session, model=Metiz)
    return templates.TemplateResponse("/finded/metizes.html", {'request': request, "metizes": res_search})


@router.get('/{object_id}', response_model=None, response_model_by_alias=True)
async def search_metiz_by_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        object_id: int,
):
    object_search = await get_object_by_id(session=session, request_id=object_id, model=Metiz)
    if object_search:
        return object_search
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"object with {object_id} not found")


@router.delete('/{metiz_id}')
async def delete_metiz(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        delete_id: int,
):
    delete_metiz = await get_object_by_id(session=session, request_id=delete_id, model=Metiz)
    if not delete_metiz:
        raise HTTPException(status_code=404, detail="Metiz not found")
    await session.delete(delete_metiz)
    await session.commit()
    return {"message": f"metiz with id={delete_id} was deleted"}


@router.put('/{metiz_id}')
async def update_metiz_by_id(
        metiz_updated: MetizUpdatePartial,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        metiz_id: int,
):
    metiz = await get_object_by_id(request_id=metiz_id, session=session, model=Metiz)
    return await update_object(
        session=session,
        object_updating=metiz_updated,
        object_for_update=metiz,
    )
