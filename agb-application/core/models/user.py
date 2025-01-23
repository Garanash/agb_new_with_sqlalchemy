from sqlalchemy.orm import mapped_column, Mapped

from .base import Base


class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
