from sqlalchemy import Column, String, Boolean

from .base import Base


class Purchased(Base):
    number_in_catalog = Column(String(50), unique=True, default='-')
    number_in_catalog_agb = Column(String(50), unique=True, default='-')
    name_in_catalog = Column(String(50), default='-')
    name_in_catalog_agb = Column(String(50), default='-')
    assigned = Column(String(50), default='-', nullable=False)  # присвоил
    name_in_KD = Column(String(50), default='-')  # имя в КД
    name_in_OEM = Column(String(50), default='-')  # имя в OEM
    note = Column(String(50), default='-')  # примечание
    date = Column(String(50), default='-')  # дата присвоения
    applicability = Column(String(50), default='-')  # применяемость

    marked_for_deletion = Column(Boolean, default=False)
