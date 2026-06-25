from sqlalchemy.orm import Session

from app.exceptions import EntityNotFoundError
from app.models.cattle import Cattle, GenderEnum
from app.repositories.cattle import CattleRepository
from app.schemas.cattle import CattleCreate, CattleUpdate, BirthCreate


class CattleDomain:
    def __init__(self, db: Session):
        self._repo = CattleRepository(db)

    def get_cattle_by_id(self, cattle_id: int) -> Cattle:
        cattle = self._repo.get_by_id(cattle_id)
        if cattle is None:
            raise EntityNotFoundError(f"Gado com ID {cattle_id} não encontrado.")
        return cattle

    def get_all_cattle(self, skip: int = 0, limit: int = 1000) -> list[Cattle]:
        return self._repo.get_all(skip=skip, limit=limit)

    def get_cattle_count(self) -> dict:
        return {"total_count": self._repo.count()}

    def get_births_by_month(self, year: int) -> dict:
        rows = self._repo.count_births_by_month(year)
        male = [0] * 12
        female = [0] * 12
        for month, gender, count in rows:
            index = int(month) - 1
            if gender == GenderEnum.MALE:
                male[index] = count
            else:
                female[index] = count
        return {"male": male, "female": female}

    def create_cattle(self, data: CattleCreate) -> Cattle:
        self._validate_parent(data.mother_id, GenderEnum.FEMALE, "mãe")
        self._validate_parent(data.father_id, GenderEnum.MALE, "pai")
        instance = Cattle(**data.model_dump())
        return self._repo.create(instance)

    def create_birth(self, data: BirthCreate) -> Cattle:
        mother = self._repo.get_by_id(data.mother_id)
        if not mother or mother.gender != GenderEnum.FEMALE:
            raise ValueError(f"Vaca mãe com ID {data.mother_id} não encontrada ou não é uma fêmea.")

        if data.father_id:
            self._validate_parent(data.father_id, GenderEnum.MALE, "pai")

        calf_race = data.race if data.race else mother.race
        instance = Cattle(
            name=data.name,
            race=calf_race,
            gender=data.gender,
            birth_date=data.birth_date,
            mother_id=data.mother_id,
            father_id=data.father_id,
            notes=data.notes,
            status="ACTIVE",
        )
        return self._repo.create(instance)

    def delete_cattle(self, cattle_id: int) -> None:
        cattle = self.get_cattle_by_id(cattle_id)
        self._repo.soft_delete(cattle)

    def update_cattle(self, cattle_id: int, data: CattleUpdate) -> Cattle:
        db_cattle = self.get_cattle_by_id(cattle_id)
        update_data = data.model_dump(exclude_unset=True)

        if "mother_id" in update_data and update_data["mother_id"] is not None:
            if update_data["mother_id"] == cattle_id:
                raise ValueError("Um animal não pode ser sua própria mãe.")
            self._validate_parent(update_data["mother_id"], GenderEnum.FEMALE, "mãe")

        if "father_id" in update_data and update_data["father_id"] is not None:
            if update_data["father_id"] == cattle_id:
                raise ValueError("Um animal não pode ser seu próprio pai.")
            self._validate_parent(update_data["father_id"], GenderEnum.MALE, "pai")

        if update_data.get("gender") == GenderEnum.MALE and db_cattle.gender == GenderEnum.FEMALE:
            if self._repo.female_has_calves(cattle_id):
                raise ValueError(
                    "Não é possível alterar o gênero para 'MALE' porque esta fêmea já possui bezerros registrados."
                )

        return self._repo.update(db_cattle, update_data)

    def _validate_parent(self, parent_id: int | None, expected_gender: GenderEnum, label: str) -> None:
        if parent_id is None:
            return
        parent = self._repo.get_by_id(parent_id)
        if not parent or parent.gender != expected_gender:
            raise ValueError(f"Animal com ID {parent_id} não encontrado ou não pode ser registrado como {label}.")
