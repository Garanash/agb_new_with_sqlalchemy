from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import (RWD, Metiz, Purchased, PurchasedHydroperforator,
                         AdaptersAndPlugs, AccordingToTheDrawing)
from api.api_v1.crud.crud_base import CRUDBase
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


@router.get('/search_all')
async def search_all_tables(
    request_item: str,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    search_results = {}
    for model in MODELS.keys():
        result = await CRUDBase(model).search(
            request=request_item,
            session=session
            )
        search_results[MODELS[model]] = len(result)
    return search_results
