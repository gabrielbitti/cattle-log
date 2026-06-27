from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.domain.cattle_reproduction_domain import CattleReproductionDomain
from app.exceptions import EntityNotFoundError
from app.schemas.cattle_reproduction import (
    CattleReproductionCreate,
    CattleReproductionUpdate,
    CattleReproductionResponse,
)

router = APIRouter(
    tags=["Cattle Reproduction"],
    responses={404: {"description": "Not found"}},
)


@router.get("/cattle-reproduction", response_model=List[CattleReproductionResponse])
def list_reproduction_endpoint(cattle_id: int | None = None, db: Session = Depends(get_db)):
    return CattleReproductionDomain(db).get_all(cattle_id=cattle_id)


@router.post("/cattle-reproduction", response_model=CattleReproductionResponse)
def create_reproduction_endpoint(data: CattleReproductionCreate, db: Session = Depends(get_db)):
    try:
        return CattleReproductionDomain(db).create(data=data)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/cattle-reproduction/{repro_id}", response_model=CattleReproductionResponse)
def update_reproduction_endpoint(
    repro_id: int, data: CattleReproductionUpdate, db: Session = Depends(get_db)
):
    try:
        return CattleReproductionDomain(db).update(repro_id=repro_id, data=data)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/cattle-reproduction/{repro_id}", status_code=204)
def delete_reproduction_endpoint(repro_id: int, db: Session = Depends(get_db)):
    try:
        CattleReproductionDomain(db).delete(repro_id=repro_id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
