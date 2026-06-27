from datetime import date
from typing import Optional

from pydantic import BaseModel

from app.models.cattle import GenderEnum
from app.models.cattle_reproduction import ReproductiveEventEnum


class CattleReproductionBase(BaseModel):
    event_type: ReproductiveEventEnum
    event_date: date
    partner_id: Optional[int] = None
    offspring_id: Optional[int] = None
    pregnancy_confirmed: Optional[bool] = None
    expected_birth_date: Optional[date] = None
    notes: Optional[str] = None


class CattleReproductionCreate(CattleReproductionBase):
    cattle_id: int
    calf_name: Optional[str] = None
    calf_gender: Optional[GenderEnum] = None
    calf_identification: Optional[str] = None


class CattleReproductionUpdate(BaseModel):
    event_type: Optional[ReproductiveEventEnum] = None
    event_date: Optional[date] = None
    partner_id: Optional[int] = None
    offspring_id: Optional[int] = None
    pregnancy_confirmed: Optional[bool] = None
    expected_birth_date: Optional[date] = None
    notes: Optional[str] = None


class CattleReproductionResponse(CattleReproductionBase):
    id: int
    cattle_id: int
    created_at: date
    updated_at: Optional[date] = None

    model_config = {"from_attributes": True}
