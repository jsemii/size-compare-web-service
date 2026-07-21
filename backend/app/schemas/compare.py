from pydantic import BaseModel

class CompareItem(BaseModel):
    field: str
    my_cloth: float | None = None
    wish_cloth: float | None = None
    diff: float | None = None
    message: str
    comparable: bool

class CompareResponse(BaseModel):
    unit: str
    my_garment_name: str
    wish_item_name: str
    items: list[CompareItem]
    compared_count: int
    missing_count: int
