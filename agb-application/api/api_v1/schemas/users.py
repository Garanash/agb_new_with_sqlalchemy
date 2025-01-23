from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=16)
    password: str = Field(min_length=3, max_length=16)
    role: str = Field(min_length=1)
    is_active: bool
    super_user: bool
    # tnum: int (табельный номер, при необходимости)

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

class UserUpdate(UserBase):
    id: int

class UserUpdatePartial(UserBase):
    id: int
    username: str | None = None
    password: str | None = None
    role: str | None = None
    is_active: bool | None = None
    super_user: bool | None = None