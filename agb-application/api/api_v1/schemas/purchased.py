from pydantic import BaseModel, Field


class PurchasedBase(BaseModel):
    number_in_catalog_agb: str = Field(min_length=3, max_length=50)
    name_in_catalog: str = Field(min_length=3, max_length=50)
    name_in_KD: str = Field(min_length=3, max_length=50)
    name_in_catalog_agb: str = Field(min_length=3, max_length=50)
    name_in_OEM: str = Field(min_length=3, max_length=50)
    assigned: str = Field(min_length=3, max_length=50)
    date: str = Field(min_length=3, max_length=50)
    applicability: str = Field(min_length=3, max_length=50)
    note: str = Field(min_length=3, max_length=50)

    marked_for_deletion: bool = Field(default=False)


class PurchasedCreate(PurchasedBase):
    number_in_catalog_agb: str | None = None
    name_in_catalog: str | None = None
    name_in_KD: str | None = None
    name_in_catalog_agb: str | None = None
    name_in_OEM: str | None = None
    assigned: str | None = None
    date: str | None = None
    applicability: str | None = None
    note: str | None = None


class PurchasedRead(PurchasedBase):
    id: int


class PurchasedUpdate(PurchasedBase):
    id: int


class PurchasedUpdatePartial(PurchasedBase):
    id: int | None = None
    number_in_catalog_agb: str | None = None
    name_in_catalog: str | None = None
    name_in_KD: str | None = None
    name_in_catalog_agb: str | None = None
    name_in_OEM: str | None = None
    assigned: str | None = None
    date: str | None = None
    applicability: str | None = None
    note: str | None = None

    marked_for_deletion: bool | None = None


class PurchasedDelete(PurchasedBase):
    id: int
