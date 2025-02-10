from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=16)
    password: str = Field(min_length=3, max_length=16)
    role: str = Field(min_length=1)
    name: str = Field(min_length=1, max_length=50)
    surname: str = Field(min_length=1, max_length=50)
    patronymic: str = Field(min_length=1, max_length=50)
    image_url: str = Field(min_length=1)
    is_active: bool = Field(default=False)
    super_user: bool = Field(default=False)
    # tnum: int (табельный номер, при необходимости)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int


class UserUpdate(UserBase):
    id: int


class UserUpdatePartial(UserBase):
    id: int | None = None
    username: str | None = None
    password: str | None = None
    role: str | None = None
    name: str | None = None
    surname: str | None = None
    patronymic: str | None = None
    image_url: str | None = None
    is_active: bool | None = None
    super_user: bool | None = None


class UserDelete(UserBase):
    id: int
