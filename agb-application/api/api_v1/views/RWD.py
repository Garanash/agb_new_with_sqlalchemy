from typing import Annotated
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from api.api_v1.schemas.RWD import RWDCreate, RWDDelete, RWDRead, RWDUpdate, RWDUpdatePartial, RWDBase
from core.models import db_helper, RWD
from api.api_v1.crud.CRUD import get_all_objects, create_new_object, update_object, get_object_by_id, delete_object, \
    search_by_request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates('templates')
router = APIRouter(
    tags=['RWDBases'],
)
@router.get('/RWDs', response_model_by_alias=True)
async def get_rwd(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request
):
    """
    вывод всех РВД в таблице
    :parameter:
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    rwd = await get_all_objects(session=session, model=RWD)
    return templates.TemplateResponse('/search/rwd.html', {"request": request, "rwd": rwd})


@router.get('/', response_model_by_alias=True)
async def get_rwd_item(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    rwd_item = await get_all_objects(session=session, model=RWD)
    return rwd_item

@router.get("/addnew")
async def add_new_rwd(request: Request):
    return templates.TemplateResponse("/addnew/add_new_rwd.html",
                                      {"request": request,
                                       "current_datetime": datetime.now().strftime("%Y-%m-%dT%H:%M")})


@router.get("/patch/{item_id}")
async def patch_rwd_by_id(request: Request, item_id: int,
                            session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    patch_item = await get_object_by_id(session=session, model=RWD, request_id=item_id)

    return templates.TemplateResponse("/patch/patch_rwd.html",
                                      {"request": request,
                                       "current_datetime": datetime.now().strftime("%Y-%m-%dT%H:%M"),
                                       "item": patch_item})


@router.post("/patch", response_class= RedirectResponse)
async def patch_rwd(
        patch_item: Annotated[RWDUpdatePartial, Form()],
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request):
    object_for_update = await get_object_by_id(request_id=patch_item.id, session=session, model=RWD)
    await update_object(session=session, object_for_update=object_for_update, object_updating=patch_item, partial=True)
    return RedirectResponse("/RWD/RWDs", status_code=301)


@router.post("/create", response_model=None, response_model_by_alias=True, response_class=RedirectResponse)
async def create_rwd(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        rwd_create: Annotated[RWDCreate, Form()],
        request: Request):
    try:
        rwd = await create_new_object(session=session, object_create=rwd_create, model=RWD)
        return RedirectResponse("/RWD/RWDs", status_code=301)

    except BaseException:
        return templates.TemplateResponse("/search/rwd.html",
                                          {'request': request, "message": "Такая деталь уже существует"})
        # return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="rwd already exists")


@router.get('/search')
async def search_rwd_by_request(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request
):
    search_item = request.query_params.get('main_input')
    res_search = await search_by_request(request=search_item, session=session, model=RWD)
    return templates.TemplateResponse("/finded/rwds.html", {'request': request, "rwds": res_search})



@router.get('/{rwd_item_id}', response_model=None, response_model_by_alias=True)
async def search_rwd_item_by_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        rwd_item_id: int,
):
    object_search = await get_object_by_id(session=session, request_id=rwd_item_id, model=RWD)
    if object_search:
        return object_search
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"object with {rwd_item_id} not found")


@router.delete('/{rwd_item_id}')
async def delete_rwd_item(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        delete_id: int,
):
    delete_rwd_item = await get_object_by_id(session=session, request_id=delete_id, model=RWD)
    if not delete_rwd_item:
        raise HTTPException(status_code=404, detail="RWD not found")
    await session.delete(delete_rwd_item)
    await session.commit()
    return {"message": f"rwd_item with id={delete_id} was deleted"}


@router.put('/{rwd_item_id}')
async def update_rwd_item_by_id(
        rwd_item_updated: RWDUpdatePartial,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        rwd_item_id: int,
):
    rwd_item = await get_object_by_id(request_id=rwd_item_id, session=session, model=RWD)
    return await update_object(
        session=session,
        object_updating=rwd_item_updated,
        object_for_update=rwd_item,
    )


# @router.get('/s/{request_item}')
# async def search_rwd_by_request(
#         request_item: str,
#         session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
# ):
#     return await search_by_request(request=request_item, session=session, model=RWD)