from sqlalchemy import Column, String, Boolean
from .base import Base


class RWD(Base):
    number = Column(String(50), unique=True, default='-')
    date = Column(String(50), default='-')
    article_number_agb = Column(String(50), default='-')
    nomenclature = Column(String(50), default='-', unique=True)
    note = Column(String(50), default='-')  # примечание
    marked_for_deletion = Column(Boolean, default=False)
