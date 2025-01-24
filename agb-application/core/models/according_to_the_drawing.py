from sqlalchemy import Column, String, Boolean
from .base import Base


class AccordingToTheDrawing(Base):
    name = Column(String(50), default='-')
    number_in_catalog = Column(String(50), unique=True, default='-')
    number_in_catalog_agb = Column(String(50), unique=True, default='-')
    name_in_catalog = Column(String(50), default='-')
    applicability = Column(String(50), default='-')  # первичное применение
    note = Column(String(50), default='-')  # примечание
    developed = Column(String(50), default='-', nullable=False)  # разработал
    KD = Column(String(50), default='-')
    date = Column(String(50), default='-')

    marked_for_deletion = Column(Boolean, default=False)
