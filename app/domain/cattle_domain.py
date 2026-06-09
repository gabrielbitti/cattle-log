"""."""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.cattle import CattleDTO
from app.schemas.cattle import CattleCreate
from app.models.cattle import Cattle


class CattleDomain:
    """."""

    def __init__(self, db: Session):
        """."""
        self.db = db

    def create_cattle(self, data: CattleCreate):
        """."""
        if data.mother_id:
            mother = CattleDTO(self.db).get_by_id(data.mother_id)
            if not mother or mother.gender != "FEMALE":
                raise ValueError(f"Vaca mãe com ID {data.mother_id} não encontrada ou não é uma fêmea.")

        if data.father_id:
            father = CattleDTO(self.db).get_by_id(data.father_id)
            if not father or father.gender != "MALE":
                raise ValueError(f"Pai com ID {data.father_id} não encontrado ou não é um macho.")

        return CattleDTO(self.db).create_cattle_in_database(data)

    def create_birth(self, data):
        """."""
        mother = self.get_by_id(data.mother_id)
        if not mother or mother.gender != "FEMALE":
            raise ValueError(
                f"Vaca mãe com ID {data.mother_id} não encontrada ou não é uma fêmea.")

        # Validate father if provided
        if data.father_id:
            father = self.get_by_id(data.father_id)
            if not father or father.gender != "MALE":
                raise ValueError(
                    f"Pai com ID {data.father_id} não encontrado ou não é um macho.")

        # Set default race from mother if not provided
        calf_race = data.race if data.race else mother.race

        # Create the calf record
        db_calf = Cattle(
            name=data.name,
            race=calf_race,
            gender=data.gender,
            birth_date=data.data_date,
            mother_id=data.mother_id,
            father_id=data.father_id,
            notes=data.notes,
            status="ACTIVE"
        )

        return CattleDTO(self.db).create_birth(db_calf)

    def get_all_cattle(self, data):
        """."""
        pass

    def get_cattle_by_id(self, cattle_id):
        """."""
        db_cattle = CattleDTO(self.db).get_by_id(cattle_id=cattle_id)
        if db_cattle is None:
            raise HTTPException(status_code=404, detail="Gado não encontrado")
        return db_cattle

    def update_cattle(self, cattle_id, data):
        """."""
        db_cattle = CattleDTO(self.db).get_by_id(cattle_id)
        if db_cattle is None:
            raise HTTPException(status_code=404, detail="Gado não encontrado")

        update_data = data.model_dump(exclude_unset=True)

        if "mother_id" in update_data and update_data["mother_id"] is not None:
            if update_data["mother_id"] == cattle_id:
                raise ValueError("Um animal não pode ser sua própria mãe.")
            mother = CattleDTO(self.db).get_by_id(update_data["mother_id"])
            if not mother or mother.gender != "FEMALE":
                raise ValueError(f"Vaca mãe com ID {update_data['mother_id']} não encontrada ou não é uma fêmea.")

        if "father_id" in update_data and update_data["father_id"] is not None:
            if update_data["father_id"] == cattle_id:
                raise ValueError("Um animal não pode ser seu próprio pai.")
            father = CattleDTO(self.db).get_by_id(update_data["father_id"])
            if not father or father.gender != "MALE":
                raise ValueError(f"Pai com ID {update_data['father_id']} não encontrado ou não é um macho.")

        if "gender" in update_data and update_data["gender"] == "MALE" and db_cattle.gender == "FEMALE":
            has_calves = CattleDTO(self.db).female_has_calves(cattle_id)
            if has_calves:
                raise ValueError("Não é possível alterar o gênero para 'MALE' porque esta fêmea já possui bezerros registrados.")

        return CattleDTO(self.db).update(db_cattle, update_data)