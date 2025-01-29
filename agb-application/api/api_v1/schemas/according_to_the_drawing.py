from pydantic import BaseModel, Field


class AccordingToTheDrawBase(BaseModel):
    name: str | None = None
    number_in_catalog: str | None = None
    number_in_catalog_agb: str | None = None
    name_in_catalog: str | None = None
    first_applicability: str | None = None
    note: str | None = None
    developed: str | None = None
    KD: str | None = None
    date: str | None = None

    marked_for_deletion: bool = Field(default=False)


class AccordingToTheDrawCreate(AccordingToTheDrawBase):
    name: str | None = None
    number_in_catalog: str | None = None
    number_in_catalog_agb: str | None = None
    name_in_catalog: str | None = None
    first_applicability: str | None = None
    note: str | None = None
    developed: str | None = None
    KD: str | None = None
    date: str | None = None


class AccordingToTheDrawRead(AccordingToTheDrawBase):
    id: int


class AccordingToTheDrawUpdate(AccordingToTheDrawBase):
    id: int


class AccordingToTheDrawUpdatePartial(AccordingToTheDrawBase):
    id: int | None = None
    name: str | None = None
    number_in_catalog: str | None = None
    number_in_catalog_agb: str | None = None
    name_in_catalog: str | None = None
    applicability: str | None = None
    note: str | None = None
    developed: str | None = None
    KD: str | None = None
    date: str | None = None

    marked_for_deletion: bool | None = None


class AccordingToTheDrawDelete(AccordingToTheDrawBase):
    id: int
