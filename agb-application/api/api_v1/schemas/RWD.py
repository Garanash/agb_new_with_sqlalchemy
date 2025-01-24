from pydantic import BaseModel, Field


class RWDBase(BaseModel):
    number: str = Field(min_length=3, max_length=50)
    date: str = Field(min_length=3, max_length=50)
    article_number_agb: str = Field(min_length=3, max_length=50)
    nomenclature: str = Field(min_length=3, max_length=50)
    note: str = Field(min_length=3, max_length=50)

class RWDCreate(RWDBase):
    pass


class RWDRead(RWDBase):
    id: int


class RWDUpdate(RWDBase):
    id: int


class RWDUpdatePartial(RWDBase):
    id: int | None = None
    number: str | None = None
    date: str | None = None
    article_number_agb: str | None = None
    nomenclature: str | None = None
    note: str | None = None


class RWDDelete(RWDBase):
    id: int
