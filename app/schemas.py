from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class CattleBase(BaseModel):
    weight: Optional[float] = Field(None, gt=0)
    birth_date: Optional[date] = None
    mother_id: Optional[int] = Field(None, gt=0)
    type: str # \'cow\' or \'bull\'

class CattleCreate(CattleBase):
    name: str
    type: str = Field(..., pattern="^(cow|bull)$") # Ensure type is cow or bull

class CattleUpdate(BaseModel):
    name: Optional[str] = Field(None)
    weight: Optional[float] = Field(None, gt=0)
    birth_date: Optional[date] = None
    mother_id: Optional[int] = Field(None, gt=0)
    type: Optional[str] = Field(None, pattern="^(cow|bull)$")

class Cattle(CattleBase):
    id: int

    class Config:
        from_attributes = True # For Pydantic v2

class BirthCreate(BaseModel):
    name:str
    type: Optional[str] = Field(None, pattern="^(cow|bull)$")
    calf_weight: Optional[float] = Field(None, gt=0)
    calf_birth_date: date
    mother_id: int = Field(..., gt=0)

class CattleCount(BaseModel):
    total_count: int

