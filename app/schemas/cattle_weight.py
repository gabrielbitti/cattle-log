"""."""

from datetime import date
from typing import Optional

from pydantic import BaseModel


class CattleWeightCreate(BaseModel):
    cattle_id: int
    measurement_date: date
    weight: float
    notes: Optional[str] = None


class CattleWeightUpdate(BaseModel):
    measurement_date: date
    weight: float
    notes: Optional[str] = None
