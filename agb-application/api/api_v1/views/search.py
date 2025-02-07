from typing import Annotated
from api.api_v1.auth.views import check_user
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession


from api.api_v1.crud.crud_base import CRUDBase
from core.models import (RWD, Metiz, Purchased, PurchasedHydroperforator,
                         AdaptersAndPlugs, AccordingToTheDrawing)
from core.models import db_helper

templates = Jinja2Templates('templates')

MODELS = {
    RWD: 'РВД',
    Metiz: 'Метизы',
    Purchased: 'Покупные детали',
    PurchasedHydroperforator: 'Гидравлические перфораторы',
    AdaptersAndPlugs: 'Адаптеры',
    AccordingToTheDrawing: 'Чертежи',
}

MODELS_PREFIX = {
    "РВД": '/RWD',
    'Метизы': '/metiz',
    'Покупные детали': '/purchased',
    'Гидравлические перфораторы': '/hydroperfs',
    'Адаптеры': '/adapters',
    'Чертежи': '/draw',
}

router = APIRouter(
    # prefix='/search'
)


@router.get('/search_rwd')
def rwd_search(request: Request):
    return templates.TemplateResponse('/search/rwd.html',
                                      {'request': request})


@router.get('/search_metizes')
def metizes_search(request: Request):
    return templates.TemplateResponse('/search/metizes.html',
                                      {'request': request})


@router.get('/search_drawing')
def drawing_search(request: Request):
    return templates.TemplateResponse('/search/drawing.html',
                                      {'request': request})


@router.get('/search_projects')
def project_search(request: Request):
    return templates.TemplateResponse('/search/projects.html',
                                      {'request': request})


@router.get('/search_purchased')
def purchased_search(request: Request):
    return templates.TemplateResponse('/search/purchased.html',
                                      {'request': request})


@router.get('/search_hydroperfs')
def purchasedhydro_search(request: Request):
    return templates.TemplateResponse('/search/hydroperfs.html',
                                      {'request': request})


@router.get('/search_adapters')
def adapter_search(request: Request):
    return templates.TemplateResponse('/search/adapters.html',
                                      {'request': request})


@router.get('/search_all_tables', dependencies=[Depends(check_user)])
async def search_all_tables(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        request: Request

):
    search_item = request.query_params.get('main_input')
    search_results = {}
    for model in MODELS.keys():
        result = await CRUDBase(model).search(
            request=search_item,
            session=session
        )
        search_results[MODELS[model]] = (len(result), model.__name__)

    class ReturnData:
        def __init__(self, table_name, count_res, prefix):
            self.table_name: str = table_name
            self.count_res: int = count_res
            self.prefix: str = prefix

    server_url = request.url.scheme + "://" + request.url.netloc
    result_data = [ReturnData(key, val[0], MODELS_PREFIX[key]) for key, val in search_results.items()]
    return templates.TemplateResponse('/finded/all_tables.html',
                                      {"request": request, "result_search": result_data, "main_input": search_item,
                                       "server_url": server_url})
