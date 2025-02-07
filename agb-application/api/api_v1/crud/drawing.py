from api.api_v1.crud.crud_base import CRUDBase
from core.models import AccordingToTheDrawing


class DrawingCRUD(CRUDBase):
    """"""
    pass


drawing_crud = DrawingCRUD(AccordingToTheDrawing)