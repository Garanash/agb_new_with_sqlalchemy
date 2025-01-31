from typing import Annotated
from datetime import datetime
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request
from fastapi.responses import RedirectResponse
from api.api_v1.schemas.according_to_the_drawing import AccordingToTheDrawRead, AccordingToTheDrawCreate, \
    AccordingToTheDrawUpdatePartial, AccordingToTheDrawBase, AccordingToTheDrawDelete
from core.models import db_helper, AccordingToTheDrawing
from api.api_v1.crud.CRUD import get_all_objects, create_new_object, update_object, get_object_by_id, delete_object, \
    search_by_request

templates = Jinja2Templates('templates')
router = APIRouter(
    tags=['AccordingToTheDrawBases'],
)


@router.get('/drawings', response_model_by_alias=True)
async def get_drawings(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request
):
    """
    вывод всех метизов в таблице
    :parameter:
    session: сессия в асинхронную базу данных
    request: запрос от пользователя
    """
    drawings = await get_all_objects(session=session, model=AccordingToTheDrawing)
    return templates.TemplateResponse('/search/drawing.html', {"request": request, "drawings": drawings})


@router.get("/addnew")
async def add_new_drawing(request: Request):
    return templates.TemplateResponse("/addnew/add_new_drawing.html",
                                      {"request": request,
                                       "current_datetime": datetime.now().strftime("%Y-%m-%dT%H:%M")})


@router.post("/patch", response_class=RedirectResponse)
async def patch_drawing(
        patch_item: Annotated[AccordingToTheDrawUpdatePartial, Form()],
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request):
    object_for_update = await get_object_by_id(request_id=patch_item.id, session=session, model=AccordingToTheDrawing)
    print(object_for_update.__dict__)

    await update_object(session=session, object_for_update=object_for_update, object_updating=patch_item, partial=True)
    return RedirectResponse("/draw/drawings", status_code=301)


@router.get('/search')
async def search_drawing_by_request(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request
):
    search_item = request.query_params.get('main_input')
    res_search = await search_by_request(request=search_item, session=session, model=AccordingToTheDrawing)
    return templates.TemplateResponse("/finded/drawing.html", {'request': request, "drawings": res_search})



@router.get("/patch/{item_id}")
async def patch_drawing_by_id(request: Request, item_id: int,
                              session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    patch_item = await get_object_by_id(session=session, model=AccordingToTheDrawing, request_id=item_id)

    return templates.TemplateResponse("/patch/patch_drawing.html",
                                      {"request": request,
                                       "current_datetime": datetime.now().strftime("%Y-%m-%dT%H:%M"),
                                       "item": patch_item})


@router.post("/create", response_model=None, response_model_by_alias=True, response_class=RedirectResponse)
async def create_drawing(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        drawing_create: Annotated[AccordingToTheDrawCreate, Form()],
        request: Request):
    try:
        drawing = await create_new_object(session=session, object_create=drawing_create, model=AccordingToTheDrawing)
        return RedirectResponse("/draw/drawings", status_code=301)
    except BaseException as ex:
        print(ex)
        return templates.TemplateResponse("/search/drawing.html",
                                          {'request': request, "message": "Такая деталь уже существует"})
        # return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="metiz already exists")



@router.get('/', response_model_by_alias=True)
async def get_according_to_the_draws(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    according_to_the_draws = await get_all_objects(session=session, model=AccordingToTheDrawing)
    return according_to_the_draws


@router.post("/new_according_to_the_draw", response_model=None, response_model_by_alias=True)
async def create_according_to_the_draw(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        according_to_the_draw_create: AccordingToTheDrawCreate):
    according_to_the_draw = await create_new_object(session=session, object_create=according_to_the_draw_create,
                                                    model=AccordingToTheDrawing)
    return according_to_the_draw


@router.get('/{object_id}', response_model=None, response_model_by_alias=True)
async def search_according_to_the_draw_by_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        object_id: int,
):
    object_search = await get_object_by_id(session=session, request_id=object_id, model=AccordingToTheDrawing)
    if object_search:
        return object_search
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"object with {object_id} not found")


@router.delete('/{according_to_the_draw_id}')
async def delete_according_to_the_draw(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        delete_id: int,
):
    delete_according_to_the_draw = await get_object_by_id(session=session, request_id=delete_id,
                                                          model=AccordingToTheDrawing)
    if not delete_according_to_the_draw:
        raise HTTPException(status_code=404, detail="AccordingToTheDraw not found")
    await session.delete(delete_according_to_the_draw)
    await session.commit()
    return {"message": f"according_to_the_draw with id={delete_id} was deleted"}


@router.put('/{according_to_the_draw_id}')
async def update_according_to_the_draw_by_id(
        according_to_the_draw_updated: AccordingToTheDrawUpdatePartial,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        according_to_the_draw_id: int,
):
    according_to_the_draw = await get_object_by_id(request_id=according_to_the_draw_id, session=session,
                                                   model=AccordingToTheDrawing)
    return await update_object(
        session=session,
        object_updating=according_to_the_draw_updated,
        object_for_update=according_to_the_draw,
    )


@router.get('/s/{request_item}')
async def search_according_by_request(
        request_item: str,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    return await search_by_request(request=request_item, session=session, model=AccordingToTheDrawing)
