from api.api_v1.crud.crud_base import CRUDBase
from core.models import AdaptersAndPlugs


class AdapterCRUD(CRUDBase):
    """"""
    pass


adapter_crud = AdapterCRUD(AdaptersAndPlugs)
