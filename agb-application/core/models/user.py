from sqlalchemy import Column, Integer, String, Boolean
from .base import Base


class User(Base):
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    role = Column(String(50), nullable=False)
    is_active = Column(Boolean)
    super_user = Column(Boolean)
    # tabel_num = Column(Integer) Табельный номер если нужен будет