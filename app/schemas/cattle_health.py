"""."""

from datetime import date
from typing import Optional

from pydantic import BaseModel

from app.models.cattle_health import HealthRecordTypeEnum


class CattleHealthCreate(BaseModel):
    cattle_id: int
    record_type: HealthRecordTypeEnum
    date: date
    description: str
    veterinarian: Optional[str] = None
    medication: Optional[str] = None
    dosage: Optional[str] = None
    cost: float
    next_dose_date: Optional[date] = None
    notes: Optional[str] = None


class CattleHealthUpdate(BaseModel):
    record_type: HealthRecordTypeEnum
    date: date
    description: str
    veterinarian: Optional[str] = None
    medication: Optional[str] = None
    dosage: Optional[str] = None
    cost: float
    next_dose_date: Optional[date] = None
    notes: Optional[str] = None
