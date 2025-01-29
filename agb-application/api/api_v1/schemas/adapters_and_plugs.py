from pydantic import BaseModel, Field


class AdapterAndPlugsBase(BaseModel):
    number_in_catalog: str = Field(min_length=3, max_length=50)
    number_in_catalog_agb: str = Field(min_length=3, max_length=50)
    name_in_catalog: str = Field(min_length=3, max_length=50)
    name_in_KD: str = Field(min_length=3, max_length=50)
    name_in_catalog_agb: str = Field(min_length=3, max_length=50)
    adapter_type: str = Field(min_length=3, max_length=50)
    adapter_angle: str = Field(min_length=3, max_length=50)
    exit_first: str = Field(min_length=3, max_length=50)
    exit_second: str = Field(min_length=3, max_length=50)
    center_exit: str = Field(min_length=3, max_length=50)
    name_in_OEM: str = Field(min_length=3, max_length=50)
    assigned: str = Field(min_length=3, max_length=50)
    note: str = Field(min_length=3, max_length=50)
    applicability: str = Field(min_length=3, max_length=50)
    date: str = Field(min_length=3, max_length=50)

    marked_for_deletion: bool = Field(default=False)


class AdapterAndPlugsCreate(AdapterAndPlugsBase):
    number_in_catalog: str | None = None
    number_in_catalog_agb: str | None = None
    name_in_catalog: str | None = None
    name_in_KD: str | None = None
    name_in_catalog_agb: str | None = None
    adapter_type: str | None = None
    adapter_angle: str | None = None
    exit_first: str | None = None
    exit_second: str | None = None
    center_exit: str | None = None
    name_in_OEM: str | None = None
    assigned: str | None = None
    note: str | None = None
    applicability: str | None = None
    date: str | None = None


class AdapterAndPlugsRead(AdapterAndPlugsBase):
    id: int


class AdapterAndPlugsUpdate(AdapterAndPlugsBase):
    id: int


class AdapterAndPlugsUpdatePartial(AdapterAndPlugsBase):
    id: int | None = None
    number_in_catalog: str | None = None
    number_in_catalog_agb: str | None = None
    name_in_catalog: str | None = None
    name_in_KD: str | None = None
    name_in_catalog_agb: str | None = None
    adapter_type: str | None = None
    adapter_angle: str | None = None
    exit_first: str | None = None
    exit_second: str | None = None
    center_exit: str | None = None
    name_in_OEM: str | None = None
    assigned: str | None = None
    note: str | None = None
    applicability: str | None = None
    date: str | None = None

    marked_for_deletion: bool | None = None


class AdapterAndPlugsDelete(AdapterAndPlugsBase):
    id: int
