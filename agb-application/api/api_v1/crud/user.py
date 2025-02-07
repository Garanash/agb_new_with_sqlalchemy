from api.api_v1.crud.crud_base import CRUDBase
from core.models import User


class UserCRUD(CRUDBase):
    """"""
    pass


user_crud = UserCRUD(User)
