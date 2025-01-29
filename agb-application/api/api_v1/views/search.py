from fastapi import APIRouter, Request

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates("templates")

router = APIRouter(
    # prefix='/search'
)


@router.get('/search_rwd')
def rwd_search(request: Request):
    return templates.TemplateResponse('/search/rwd.html', {'request': request})


@router.get('/search_metizes')
def metizes_search(request: Request):
    return templates.TemplateResponse('/search/metizes.html', {'request': request})


@router.get('/search_drawing')
def drawing_search(request: Request):
    return templates.TemplateResponse('/search/drawing.html', {'request': request})


@router.get('/search_projects')
def project_search(request: Request):
    return templates.TemplateResponse('/search/projects.html', {'request': request})


@router.get('/search_purchased')
def purchased_search(request: Request):
    return templates.TemplateResponse('/search/purchased.html', {'request': request})


@router.get('/search_hydroperfs')
def purchasedhydro_search(request: Request):
    return templates.TemplateResponse('/search/hydroperfs.html', {'request': request})


@router.get('/search_adapters')
def adapter_search(request: Request):
    return templates.TemplateResponse('/search/adapters.html', {'request': request})
