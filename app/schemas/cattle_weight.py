from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class CattleWeightBase(BaseModel):
    measurement_date: date
    weight: Decimal
    notes: Optional[str] = None


class CattleWeightCreate(CattleWeightBase):
    cattle_id: int


class CattleWeightUpdate(BaseModel):
    measurement_date: Optional[date] = None
    weight: Optional[Decimal] = None
    notes: Optional[str] = None


class CattleWeightResponse(CattleWeightBase):
    id: int
    cattle_id: int
    created_at: date
    updated_at: Optional[date] = None

    model_config = {"from_attributes": True}
