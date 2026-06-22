from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from app.models.cattle_health import HealthRecordTypeEnum


class CattleHealthBase(BaseModel):
    record_type: HealthRecordTypeEnum
    date: date
    description: str
    veterinarian: Optional[str] = None
    medication: Optional[str] = None
    dosage: Optional[str] = None
    cost: Optional[Decimal] = None
    next_dose_date: Optional[date] = None
    notes: Optional[str] = None


class CattleHealthCreate(CattleHealthBase):
    cattle_id: int


class CattleHealthUpdate(BaseModel):
    record_type: Optional[HealthRecordTypeEnum] = None
    date: Optional[date] = None
    description: Optional[str] = None
    veterinarian: Optional[str] = None
    medication: Optional[str] = None
    dosage: Optional[str] = None
    cost: Optional[Decimal] = None
    next_dose_date: Optional[date] = None
    notes: Optional[str] = None


class CattleHealthResponse(CattleHealthBase):
    id: int
    cattle_id: int
    created_at: date
    updated_at: Optional[date] = None

    model_config = {"from_attributes": True}
