from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database.db import get_db
from typing import List

router = APIRouter(
    tags=["Cattle Weight"],
    responses={404: {"description": "Not found"}},
)

@router.post("/cattle-weight", response_model=schemas.CattleWeightCreate, summary="Create new cattle weight")
def create_cattle_weight_endpoint(cattle_weight: schemas.CattleWeightCreate, db: Session = Depends(get_db)):
    """Creates a new cattle record (cow or bull)."""
    try:
        return crud.create_cattle_weight(db=db, cattle_weight=cattle_weight)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(e)
        # Log the exception details in a real application
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado ao criar o gado.")


@router.put("/cattle-weight/{cattle_weight_id}", response_model=schemas.CattleWeightUpdate, summary="Update cattle by ID")
def update_cattle_endpoint(cattle_weight_id: int, cattle_weight_update: schemas.CattleWeightUpdate, db: Session = Depends(get_db)):
    """Updates an existing cattle record by its ID."""
    try:
        updated_cattle = crud.update_cattle_weight(db=db, cattle_weight_id=cattle_weight_id, cattle_weight_update=cattle_weight_update)
        if updated_cattle is None:
            raise HTTPException(status_code=404, detail="Peso não encontrado")
        return updated_cattle
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado ao atualizar o gado.")