from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.domain.cattle_health_domain import CattleHealthDomain
from app.exceptions import EntityNotFoundError
from app.schemas.cattle_health import CattleHealthCreate, CattleHealthUpdate, CattleHealthResponse

router = APIRouter(
    tags=["Cattle Health"],
    responses={404: {"description": "Not found"}},
)


@router.get("/cattle-health", response_model=List[CattleHealthResponse], summary="List health records")
def list_cattle_health_endpoint(cattle_id: int | None = None, db: Session = Depends(get_db)):
    return CattleHealthDomain(db).get_all(cattle_id=cattle_id)


@router.post("/cattle-health", response_model=CattleHealthResponse, summary="Create cattle health record")
def create_cattle_health_endpoint(cattle_health: CattleHealthCreate, db: Session = Depends(get_db)):
    try:
        return CattleHealthDomain(db).create(data=cattle_health)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/cattle-health/{cattle_health_id}", response_model=CattleHealthResponse, summary="Update health record")
def update_cattle_health_endpoint(
    cattle_health_id: int, cattle_health_update: CattleHealthUpdate, db: Session = Depends(get_db)
):
    try:
        return CattleHealthDomain(db).update(health_id=cattle_health_id, data=cattle_health_update)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
