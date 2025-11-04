from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database.db import get_db
from typing import List

router = APIRouter(
    tags=["Cattle"],
    responses={404: {"description": "Not found"}},
)

@router.post("/cattle", response_model=schemas.Cattle, summary="Create new cattle")
def create_cattle_endpoint(cattle: schemas.CattleCreate, db: Session = Depends(get_db)):
    """Creates a new cattle record (cow or bull)."""
    try:
        return crud.create_cattle(db=db, cattle=cattle)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(e)
        # Log the exception details in a real application
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado ao criar o gado.")

@router.post("/cattle/birth", response_model=schemas.Cattle, summary="Register a birth")
def create_birth_endpoint(birth: schemas.BirthCreate, db: Session = Depends(get_db)):
    """Registers a new birth, creating a calf record linked to a mother cow."""
    try:
        return crud.create_birth(db=db, birth=birth)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado ao registrar o nascimento.")

@router.get("/cattle", response_model=List[schemas.Cattle], summary="List all cattle")
def read_all_cattle_endpoint(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    """Retrieves a list of all cattle records."""
    try:
        cattle_list = crud.get_all_cattle(db, skip=skip, limit=limit)
        return cattle_list
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado ao listar o gado.")

@router.get("/cattle/count", response_model=schemas.CattleCount, summary="Get total cattle count")
def get_cattle_count_endpoint(db: Session = Depends(get_db)):
    """Returns the total number of cattle records."""
    try:
        count = crud.get_cattle_count(db)
        return {"total_count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado ao contar o gado.")

@router.get("/cattle/{cattle_id}", response_model=schemas.Cattle, summary="Get cattle by ID")
def read_cattle_by_id_endpoint(cattle_id: int, db: Session = Depends(get_db)):
    """Retrieves a single cattle record by its ID."""
    try:
        db_cattle = crud.get_cattle_by_id(db, cattle_id=cattle_id)
        if db_cattle is None:
            raise HTTPException(status_code=404, detail="Gado não encontrado")
        return db_cattle
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado ao buscar o gado.")

@router.put("/cattle/{cattle_id}", response_model=schemas.Cattle, summary="Update cattle by ID")
def update_cattle_endpoint(cattle_id: int, cattle_update: schemas.CattleUpdate, db: Session = Depends(get_db)):
    """Updates an existing cattle record by its ID."""
    try:
        updated_cattle = crud.update_cattle(db=db, cattle_id=cattle_id, cattle_update=cattle_update)
        if updated_cattle is None:
            raise HTTPException(status_code=404, detail="Gado não encontrado")
        return updated_cattle
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ocorreu um erro inesperado ao atualizar o gado.")

