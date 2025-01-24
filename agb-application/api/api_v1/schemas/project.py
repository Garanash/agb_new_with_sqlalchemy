from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    classifier: str = Field(min_length=3, max_length=16)
    project: str = Field(min_length=3, max_length=16)
    is_active: bool = Field(default=True)


class ProjectCreate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    id: int


class ProjectUpdate(ProjectBase):
    id: int


class ProjectUpdatePartial(ProjectBase):
    id: int | None = None
    classifier: str | None = None
    project: str | None = None
    is_active: bool | None = None


class ProjectDelete(ProjectBase):
    id: int
