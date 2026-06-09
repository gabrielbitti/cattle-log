from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.domain.cattle_domain import CattleDomain
from app.database.db import get_db
from app.models.cattle import CattleDTO
from app.schemas.cattle import (Cattle, BirthCreate, CattleCreate, CattleCount,
                                CattleUpdate)

router = APIRouter(
    tags=["Cattle"],
    responses={404: {"description": "Not found"}},
)


@router.post("/cattle", response_model=Cattle, summary="Create new cattle")
def create_cattle_endpoint(cattle: CattleCreate, db: Session = Depends(get_db)):
    """Creates a new cattle record (cow or bull)."""
    cattle_domain = CattleDomain(db)
    return cattle_domain.create_cattle(data=cattle)


@router.post("/cattle/birth", response_model=Cattle, summary="Register a birth")
def create_birth_endpoint(birth: BirthCreate, db: Session = Depends(get_db)):
    """Registers a new birth, creating a calf record linked to a mother cow."""
    cattle_domain = CattleDomain(db)
    return cattle_domain.create_birth(data=birth)


@router.get("/cattle", response_model=List[Cattle], summary="List all cattle")
def read_all_cattle_endpoint(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    """Retrieves a list of all cattle records."""
    return CattleDTO(db).get_all(skip=skip, limit=limit)

@router.get("/cattle/count", response_model=CattleCount, summary="Get total cattle count")
def get_cattle_count_endpoint(db: Session = Depends(get_db)):
    """Returns the total number of cattle records."""
    return CattleDTO(db).get_cattle_count()

@router.get("/cattle/{cattle_id}", response_model=Cattle, summary="Get cattle by ID")
def read_cattle_by_id_endpoint(cattle_id: int, db: Session = Depends(get_db)):
    """Retrieves a single cattle record by its ID."""
    cattle_domain = CattleDomain(db)
    return cattle_domain.get_cattle_by_id(cattle_id=cattle_id)

@router.put("/cattle/{cattle_id}", response_model=Cattle, summary="Update cattle by ID")
def update_cattle_endpoint(cattle_id: int, cattle_update: CattleUpdate, db: Session = Depends(get_db)):
    """Updates an existing cattle record by its ID."""
    cattle_domain = CattleDomain(db)
    return cattle_domain.update_cattle(cattle_id=cattle_id, data=cattle_update)

