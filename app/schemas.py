"""."""

from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from app.models.cattle import GenderEnum, StatusEnum
from app.models.cattle_health import HealthRecordTypeEnum


class CattleBase(BaseModel):
    name: str
    identification: Optional[str] = None
    race: str
    gender: GenderEnum
    birth_date: Optional[date] = None
    acquisition_date: Optional[date] = None
    acquisition_value: Optional[Decimal] = Field(None, ge=0)
    status: Optional[StatusEnum] = StatusEnum.ACTIVE
    mother_id: Optional[int] = Field(None, gt=0)
    father_id: Optional[int] = Field(None, gt=0)
    origin: Optional[str] = None
    notes: Optional[str] = None


class CattleCreate(CattleBase):
    pass


class CattleUpdate(BaseModel):
    name: Optional[str] = None
    identification: Optional[str] = None
    race: Optional[str] = None
    gender: Optional[GenderEnum] = None
    birth_date: Optional[date] = None
    acquisition_date: Optional[date] = None
    acquisition_value: Optional[Decimal] = Field(None, ge=0)
    status: Optional[StatusEnum] = None
    mother_id: Optional[int] = Field(None, gt=0)
    father_id: Optional[int] = Field(None, gt=0)
    origin: Optional[str] = None
    notes: Optional[str] = None


class Cattle(CattleBase):
    id: int
    created_at: date
    updated_at: Optional[date] = None

    class Config:
        from_attributes = True


class BirthCreate(BaseModel):
    name: str
    gender: GenderEnum
    birth_date: date
    mother_id: int = Field(None, gt=0)
    father_id: Optional[int] = Field(None, gt=0)
    race: Optional[str] = None
    notes: Optional[str] = None


class CattleCount(BaseModel):
    total_count: int


class CattleWeightCreate(BaseModel):
    cattle_id: int
    measurement_date: date
    weight: float
    notes: Optional[str] = None


class CattleWeightUpdate(BaseModel):
    measurement_date: date
    weight: float
    notes: Optional[str] = None


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
