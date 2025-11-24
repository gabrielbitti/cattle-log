from sqlalchemy.orm import Session
from sqlalchemy import func
from . import schemas
from .models.cattle import Cattle


def get_cattle_by_id(db: Session, cattle_id: int):
    """Fetches a single cattle record by its ID."""
    return db.query(Cattle).filter(Cattle.id == cattle_id).first()

def get_all_cattle(db: Session, skip: int = 0, limit: int = 9999):
    """Fetches a list of cattle records, ordered by ID."""
    return db.query(Cattle).order_by(Cattle.id).offset(skip).limit(limit).all()

def create_cattle(db: Session, cattle: schemas.CattleCreate):
    """Creates a new cattle record."""
    # Validate mother if provided
    if cattle.mother_id:
        mother = get_cattle_by_id(db, cattle.mother_id)
        if not mother or mother.gender != "FEMALE":
            raise ValueError(f"Vaca mãe com ID {cattle.mother_id} não encontrada ou não é uma fêmea.")

    # Validate father if provided
    if cattle.father_id:
        father = get_cattle_by_id(db, cattle.father_id)
        if not father or father.gender != "MALE":
            raise ValueError(f"Pai com ID {cattle.father_id} não encontrado ou não é um macho.")

    db_cattle = Cattle(**cattle.model_dump()) # Use model_dump for Pydantic v2
    db.add(db_cattle)
    db.commit()
    db.refresh(db_cattle)

    return db_cattle

def update_cattle(db: Session, cattle_id: int, cattle_update: schemas.CattleUpdate):
    """Updates an existing cattle record."""
    db_cattle = get_cattle_by_id(db, cattle_id)
    if not db_cattle:
        return None # Indicate cattle not found

    update_data = cattle_update.model_dump(exclude_unset=True)

    # --- Business Logic Validations ---
    # Validate mother_id update
    if "mother_id" in update_data and update_data["mother_id"] is not None:
        if update_data["mother_id"] == cattle_id:
             raise ValueError("Um animal não pode ser sua própria mãe.")
        mother = get_cattle_by_id(db, update_data["mother_id"])
        if not mother or mother.gender != "FEMALE":
            raise ValueError(f"Vaca mãe com ID {update_data['mother_id']} não encontrada ou não é uma fêmea.")

    # Validate father_id update
    if "father_id" in update_data and update_data["father_id"] is not None:
        if update_data["father_id"] == cattle_id:
             raise ValueError("Um animal não pode ser seu próprio pai.")
        father = get_cattle_by_id(db, update_data["father_id"])
        if not father or father.gender != "MALE":
            raise ValueError(f"Pai com ID {update_data['father_id']} não encontrado ou não é um macho.")

    # Validate gender change: prevent changing a mother to male
    if "gender" in update_data and update_data["gender"] == "MALE" and db_cattle.gender == "FEMALE":
        # Check if this female has any calves
        has_calves = db.query(Cattle.id).filter(Cattle.mother_id == cattle_id).first() is not None
        if has_calves:
            raise ValueError("Não é possível alterar o gênero para 'MALE' porque esta fêmea já possui bezerros registrados.")
    # --- End Validations ---

    # Apply updates
    for key, value in update_data.items():
        setattr(db_cattle, key, value)

    db.commit()
    db.refresh(db_cattle)

    return db_cattle

def create_birth(db: Session, birth: schemas.BirthCreate):
    """Registers a birth, creating a new calf linked to a mother cow."""
    mother = get_cattle_by_id(db, birth.mother_id)
    if not mother or mother.gender != "FEMALE":
        raise ValueError(f"Vaca mãe com ID {birth.mother_id} não encontrada ou não é uma fêmea.")

    # Validate father if provided
    if birth.father_id:
        father = get_cattle_by_id(db, birth.father_id)
        if not father or father.gender != "MALE":
            raise ValueError(f"Pai com ID {birth.father_id} não encontrado ou não é um macho.")

    # Set default race from mother if not provided
    calf_race = birth.race if birth.race else mother.race

    # Create the calf record
    db_calf = Cattle(
        name=birth.name,
        race=calf_race,
        gender=birth.gender,
        birth_date=birth.birth_date,
        mother_id=birth.mother_id,
        father_id=birth.father_id,
        notes=birth.notes,
        status="ACTIVE"
    )
    db.add(db_calf)
    db.commit()
    db.refresh(db_calf)

    return db_calf

def get_cattle_count(db: Session) -> int:
    """Counts the total number of cattle records."""
    # Using count() is generally efficient for simple counts
    return db.query(func.count(Cattle.id)).scalar()

