from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.schemas.adapters_and_plugs import AdapterAndPlugsRead, AdapterAndPlugsCreate, \
    AdapterAndPlugsUpdatePartial, AdapterAndPlugsBase, AdapterAndPlugsDelete
from core.models import db_helper, AdaptersAndPlugs
from api.api_v1.crud.CRUD import get_all_objects, create_new_object, update_object, get_object_by_id, delete_object, \
    search_by_request

templates = Jinja2Templates("templates")

router = APIRouter(
    tags=['AdapterAndPlugsBases'],
)


@router.get('/adapters', response_model_by_alias=True)
async def get_adapters_and_plugss(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request
):
    adapters_and_plugs = await get_all_objects(session=session, model=AdaptersAndPlugs)
    return templates.TemplateResponse('/search/adapters.html', {"request": request, "adapters": adapters_and_plugs})


@router.get("/addnew")
async def add_new_adapter(request: Request):
    return templates.TemplateResponse("/addnew/add_new_adapter.html",
                                      {"request": request,
                                       "current_datetime": datetime.now().strftime("%Y-%m-%dT%H:%M")})


@router.get("/patch/{item_id}")
async def patch_adapter_by_id(request: Request, item_id: int,
                            session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    patch_item = await get_object_by_id(session=session, model=AdaptersAndPlugs, request_id=item_id)
    print(request.cookies.items())
    return templates.TemplateResponse("/patch/patch_adapter.html",
                                      {"request": request,
                                       "current_datetime": datetime.now().strftime("%Y-%m-%dT%H:%M"),
                                       "item": patch_item})


@router.post("/patch", response_class= RedirectResponse)
async def patch_adapters(
        patch_item: Annotated[AdapterAndPlugsUpdatePartial, Form()],
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request):
    object_for_update = await get_object_by_id(request_id=patch_item.id, session=session, model=AdaptersAndPlugs)
    await update_object(session=session, object_for_update=object_for_update, object_updating=patch_item, partial=True)
    return RedirectResponse("/adapter/adapters", status_code=301)


@router.get('/search')
async def search_adapter_by_request(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request
):
    search_item = request.query_params.get('main_input')
    res_search = await search_by_request(request=search_item, session=session, model=AdaptersAndPlugs)
    return templates.TemplateResponse("/finded/adapters.html", {'request': request, "adapters": res_search})


@router.get('/{object_id}', response_model=None, response_model_by_alias=True)
async def search_adapter_by_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        object_id: int,
):
    object_search = await get_object_by_id(session=session, request_id=object_id, model=AdaptersAndPlugs)
    if object_search:
        return object_search
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"object with {object_id} not found")


@router.delete('/{adapter_id}')
async def delete_adapter(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        delete_id: int,
):
    delete_adapter = await get_object_by_id(session=session, request_id=delete_id, model=AdaptersAndPlugs)
    if not delete_adapter:
        raise HTTPException(status_code=404, detail="adapter not found")
    await session.delete(delete_adapter)
    await session.commit()
    return {"message": f"Adapter with id={delete_id} was deleted"}


@router.put('/{adapter_id}')
async def update_adapter_by_id(
        adapter_updated: AdapterAndPlugsUpdatePartial,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        metiz_id: int,
):
    adapter = await get_object_by_id(request_id=metiz_id, session=session, model=AdaptersAndPlugs)
    return await update_object(
        session=session,
        object_updating=adapter_updated,
        object_for_update=adapter,
    )
