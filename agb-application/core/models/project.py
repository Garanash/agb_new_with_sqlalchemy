from sqlalchemy import Column, String, Boolean
from .base import Base


class Project(Base):
    classifier = Column(String(50), nullable=False, unique=True, default='-')
    project = Column(String(50), nullable=False, unique=True)

    is_active = Column(Boolean)
