from sqlalchemy import Column, String, Boolean
from .base import Base


class AdaptersAndPlugs(Base):
    number_in_catalog = Column(String(50), unique=True, default='-')
    number_in_catalog_agb = Column(String(50), unique=True, default='-')
    name_in_catalog = Column(String(50), default='-')
    name_in_KD = Column(String(50), default='-')
    name_in_catalog_agb = Column(String(50), default='-')
    adapter_type = Column(String(50), default='-')
    adapter_angle = Column(String(50), default='-')
    exit_first = Column(String(50), default='-')
    exit_second = Column(String(50), default='-')
    center_exit = Column(String(50), default='-')
    name_in_OEM = Column(String(50), default='-')
    assigned = Column(String(50), default='-', nullable=False)
    note = Column(String(50), default='-')
    applicability = Column(String(50), default='-')
    date = Column(String(50), default='-')

    marked_for_deletion = Column(Boolean, default=False)