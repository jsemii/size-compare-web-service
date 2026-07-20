from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

class GarmentCreate(BaseModel):
    name: str
    total_length_cm: Decimal | None = None
    shoulder_cm: Decimal | None = None
    chest_cm: Decimal | None = None
    sleeve_cm: Decimal | None = None
    waist_cm: Decimal | None = None
    hip_cm: Decimal | None = None
    photo_url: str | None = None

class GarmentUpdate(BaseModel):
    name: str | None = None
    total_length_cm: Decimal | None = None
    shoulder_cm: Decimal | None = None
    chest_cm: Decimal | None = None
    sleeve_cm: Decimal | None = None
    waist_cm: Decimal | None = None
    hip_cm: Decimal | None = None
    photo_url: str | None = None

class GarmentResponse(BaseModel):
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
    created_at: datetime