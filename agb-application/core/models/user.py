from sqlalchemy import Column, String, Boolean, Integer
from .base import Base


class User(Base):
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False, default="-")
    role = Column(String(50), nullable=False)
    age = Column(Integer, default=0)
    name = Column(String(50), default="-")
    surname = Column(String(50), default="-")
    patronymic = Column(String(50), default="-")
    image = Column(String(255), default="-")

    is_active = Column(Boolean)
    super_user = Column(Boolean)
    # tabel_num = Column(Integer) Табельный номер если нужен будет
