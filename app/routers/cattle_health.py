"""."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database.db import get_db

router = APIRouter(
    tags=["Cattle Health"],
    responses={404: {"description": "Not found"}},
)

@router.post("/cattle-health", response_model=schemas.CattleHealthCreate, summary="Create new cattle health")
def create_cattle_health_endpoint(cattle_health: schemas.CattleHealthCreate, db: Session = Depends(get_db)):
    """Creates a new cattle record (cow or bull)."""
    try:
        return crud.create_cattle_health(db=db, cattle_health=cattle_health)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(e)
        # Log the exception details in a real application
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado ao criar o gado.")


@router.put("/cattle-health/{cattle_health_id}", response_model=schemas.CattleHealthUpdate, summary="Update cattle by ID")
def update_cattle_health_endpoint(cattle_health_id: int, cattle_health_update: schemas.CattleHealthUpdate, db: Session = Depends(get_db)):
    """Updates an existing cattle record by its ID."""
    try:
        updated_cattle = crud.update_cattle_health(db=db, cattle_health_id=cattle_health_id, cattle_health_update=cattle_health_update)
        if updated_cattle is None:
            raise HTTPException(status_code=404, detail="Peso não encontrado")
        return updated_cattle
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado ao atualizar o gado.")