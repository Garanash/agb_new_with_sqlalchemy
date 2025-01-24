from pydantic import BaseModel, Field


class MetizBase(BaseModel):
    number_in_catalog: str = Field(min_length=3, max_length=50)
    number_in_catalog_agb: str = Field(min_length=3, max_length=50)
    name_in_catalog: str = Field(min_length=3, max_length=50)
    name_in_KD: str = Field(min_length=3, max_length=50)
    name_in_catalog_agb: str = Field(min_length=3, max_length=50)
    standard: str = Field(min_length=3, max_length=50)
    hardware_type: str = Field(min_length=3, max_length=50)
    thread_profile: str = Field(min_length=3, max_length=50)
    nominal_diameter: str = Field(min_length=3, max_length=50)
    thread_pitch: str = Field(min_length=3, max_length=50)
    length: str = Field(min_length=3, max_length=50)
    strength_class: str = Field(min_length=3, max_length=50)
    Material_or_coating: str = Field(min_length=3, max_length=50)
    assigned: str = Field(min_length=3, max_length=50)
    note: str = Field(min_length=3, max_length=50)
    applicability: str = Field(min_length=3, max_length=50)
    date: str = Field(min_length=3, max_length=50)
    marked_for_deletion: bool = Field(default=False)


class MetizCreate(MetizBase):
    pass


class MetizRead(MetizBase):
    id: int


class MetizUpdate(MetizBase):
    id: int


class MetizUpdatePartial(MetizBase):
    id: int | None = None
    number_in_catalog: str | None = None
    number_in_catalog_agb: str | None = None
    name_in_catalog: str | None = None
    name_in_KD: str | None = None
    name_in_catalog_agb: str | None = None
    standard: str | None = None
    hardware_type: str | None = None
    thread_profile: str | None = None
    nominal_diameter: str | None = None
    thread_pitch: str | None = None
    length: str | None = None
    strength_class: str | None = None
    Material_or_coating: str | None = None
    assigned: str | None = None
    note: str | None = None
    applicability: str | None = None
    date: str | None = None
    marked_for_deletion: bool | None = None


class MetizDelete(MetizBase):
    id: int
