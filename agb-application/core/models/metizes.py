from sqlalchemy import Column, String, Boolean
from .base import Base


class Metiz(Base):
    number_in_catalog = Column(String(50), unique=True, default='-')
    number_in_catalog_agb = Column(String(50), unique=True, default='-')
    name_in_catalog = Column(String(50), default='-')
    name_in_KD = Column(String(50), default='-')
    name_in_catalog_agb = Column(String(50), default='-')
    standard = Column(String(50), default='-')
    hardware_type = Column(String(50), default='-')
    thread_profile = Column(String(50), default='-')
    nominal_diameter = Column(String(50), default='-')
    thread_pitch = Column(String(50), default='-')
    length = Column(String(50), default='-')
    strength_class = Column(String(50), default='-')
    Material_or_coating = Column(String(50), default='-')
    assigned = Column(String(50), default='-', nullable=False)
    note = Column(String(50), default='-')
    applicability = Column(String(50), default='-')
    date = Column(String(50), default='-')
    marked_for_deletion = Column(Boolean, default=False)
