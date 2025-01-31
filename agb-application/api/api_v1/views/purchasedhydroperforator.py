from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.schemas.purchased_hydroperforator import PurchasedHydroperforatorRead, PurchasedHydroperforatorCreate, \
    PurchasedHydroperforatorUpdatePartial, PurchasedHydroperforatorBase, PurchasedHydroperforatorDelete
from core.models import db_helper, PurchasedHydroperforator
from api.api_v1.crud.CRUD import get_all_objects, create_new_object, update_object, get_object_by_id, delete_object, \
    search_by_request

templates = Jinja2Templates("templates")

router = APIRouter(
    tags=['PurchasedHydroperforatorBases'],
)


@router.get('/hydroperfs', response_model_by_alias=True)
async def get_hydroperforators(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request
):
    hydroperfs = await get_all_objects(session=session, model=PurchasedHydroperforator)
    return templates.TemplateResponse('/search/hydroperfs.html', {"request": request, "hyfroperfs": hydroperfs})


@router.get("/addnew")
async def add_new_hydroperforator(request: Request):
    return templates.TemplateResponse("/addnew/add_new_hydroperf.html",
                                      {"request": request,
                                       "current_datetime": datetime.now().strftime("%Y-%m-%dT%H:%M")})


@router.get("/patch/{item_id}")
async def patch_hydroperf_by_id(request: Request, item_id: int,
                                session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    patch_item = await get_object_by_id(session=session, model=PurchasedHydroperforator, request_id=item_id)
    print(request.cookies.items())
    return templates.TemplateResponse("/patch/patch_hydroperf.html",
                                      {"request": request,
                                       "current_datetime": datetime.now().strftime("%Y-%m-%dT%H:%M"),
                                       "item": patch_item})


@router.post("/patch", response_class=RedirectResponse)
async def patch_hydroperforators(
        patch_item: Annotated[PurchasedHydroperforatorUpdatePartial, Form()],
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request):
    object_for_update = await get_object_by_id(request_id=patch_item.id, session=session,
                                               model=PurchasedHydroperforator)
    await update_object(session=session, object_for_update=object_for_update, object_updating=patch_item, partial=True)
    return RedirectResponse("/hydroperfs/hydroperfs", status_code=301)


@router.post("/create", response_model=None, response_model_by_alias=True, response_class=RedirectResponse)
async def create_hydroperforator(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        adapter_create: Annotated[PurchasedHydroperforatorCreate, Form()],
        request: Request):
    try:
        adapter = await create_new_object(session=session, object_create=adapter_create, model=PurchasedHydroperforator)

        return RedirectResponse("/hydroperfs/hydroperfs", status_code=301)

    except BaseException as ex:
        print(ex)
        return templates.TemplateResponse("/search/hydroperfs.html",
                                          {'request': request, "message": "Такая деталь уже существует"})


@router.get('/search')
async def search_hydroperforator_by_request(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request
):
    search_item = request.query_params.get('main_input')
    res_search = await search_by_request(request=search_item, session=session, model=PurchasedHydroperforator)
    return templates.TemplateResponse("/finded/hydroperfs.html", {'request': request, "hydroperfs": res_search})


@router.get('/{object_id}', response_model=None, response_model_by_alias=True)
async def search_hydroperforator_by_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        object_id: int,
):
    object_search = await get_object_by_id(session=session, request_id=object_id, model=PurchasedHydroperforator)
    if object_search:
        return object_search
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"object with {object_id} not found")


@router.delete('/{hydroperf_id}')
async def delete_hydroperforator(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        delete_id: int,
):
    delete_hydroperf = await get_object_by_id(session=session, request_id=delete_id, model=PurchasedHydroperforator)
    if not delete_hydroperf:
        raise HTTPException(status_code=404, detail="Hydroperforator not found")
    await session.delete(delete_hydroperf)
    await session.commit()
    return {"message": f"Hydroperforator with id={delete_id} was deleted"}


@router.put('/{hydroperf_id}')
async def update_hydroperforator_by_id(
        hydroperf_updated: PurchasedHydroperforatorUpdatePartial,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        hydroperf_id: int,
):
    hydroperf = await get_object_by_id(request_id=hydroperf_id, session=session, model=PurchasedHydroperforator)
    return await update_object(
        session=session,
        object_updating=hydroperf_updated,
        object_for_update=hydroperf,
    )
