from api.api_v1.crud.crud_base import CRUDBase
from core.models import Purchased


class PurchasedCRUD(CRUDBase):
    """"""
    pass


purchased_crud = PurchasedCRUD(Purchased)
