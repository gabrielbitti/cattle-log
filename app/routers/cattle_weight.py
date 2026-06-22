from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.domain.cattle_weight_domain import CattleWeightDomain
from app.exceptions import EntityNotFoundError
from app.schemas.cattle_weight import CattleWeightCreate, CattleWeightUpdate, CattleWeightResponse

router = APIRouter(
    tags=["Cattle Weight"],
    responses={404: {"description": "Not found"}},
)


@router.get("/cattle-weight", response_model=List[CattleWeightResponse], summary="List weight records")
def list_cattle_weight_endpoint(cattle_id: int | None = None, db: Session = Depends(get_db)):
    return CattleWeightDomain(db).get_all(cattle_id=cattle_id)


@router.post("/cattle-weight", response_model=CattleWeightResponse, summary="Create cattle weight record")
def create_cattle_weight_endpoint(cattle_weight: CattleWeightCreate, db: Session = Depends(get_db)):
    try:
        return CattleWeightDomain(db).create(data=cattle_weight)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/cattle-weight/{cattle_weight_id}", response_model=CattleWeightResponse, summary="Update weight record")
def update_cattle_weight_endpoint(
    cattle_weight_id: int, cattle_weight_update: CattleWeightUpdate, db: Session = Depends(get_db)
):
    try:
        return CattleWeightDomain(db).update(weight_id=cattle_weight_id, data=cattle_weight_update)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
