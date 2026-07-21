from datetime import datetime
from decimal import Decimal
from pydantic import Field, BaseModel, ConfigDict

class WishlistCreate(BaseModel):
    name: str
    total_length_cm: Decimal | None = Field(default=None, gt=0)
    shoulder_cm: Decimal | None = Field(default=None, gt=0)
    chest_cm: Decimal | None = Field(default=None, gt=0)
    sleeve_cm: Decimal | None = Field(default=None, gt=0)
    waist_cm: Decimal | None = Field(default=None, gt=0)
    hip_cm: Decimal | None = Field(default=None, gt=0)
    photo_url: str | None = None
    shop_name: str | None = None
    category: str | None = None

class WishlistUpdate(BaseModel):
    name: str | None = None
    total_length_cm: Decimal | None = Field(default=None, gt=0)
    shoulder_cm: Decimal | None = Field(default=None, gt=0)
    chest_cm: Decimal | None = Field(default=None, gt=0)
    sleeve_cm: Decimal | None = Field(default=None, gt=0)
    waist_cm: Decimal | None = Field(default=None, gt=0)
    hip_cm: Decimal | None = Field(default=None, gt=0)
    photo_url: str | None = None
    shop_name: str | None = None
    category: str | None = None


class WishlistResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    total_length_cm: Decimal | None = None
    shoulder_cm: Decimal | None = None
    chest_cm: Decimal | None = None
    sleeve_cm: Decimal | None = None
    waist_cm: Decimal | None = None
    hip_cm: Decimal | None = None
    photo_url: str | None = None
    shop_name: str | None = None
    category: str | None = None
    created_at: datetime