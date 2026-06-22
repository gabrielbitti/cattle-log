from sqlalchemy.orm import Session

from app.exceptions import EntityNotFoundError
from app.models.cattle_weight import CattleWeight
from app.repositories.cattle import CattleRepository
from app.repositories.cattle_weight import CattleWeightRepository
from app.schemas.cattle_weight import CattleWeightCreate, CattleWeightUpdate


class CattleWeightDomain:
    def __init__(self, db: Session):
        self._repo = CattleWeightRepository(db)
        self._cattle_repo = CattleRepository(db)

    def get_all(self, cattle_id: int | None = None) -> list[CattleWeight]:
        if cattle_id is not None:
            return self._repo.get_all_by_cattle(cattle_id)
        return self._repo.get_all()

    def get_by_id(self, weight_id: int) -> CattleWeight:
        record = self._repo.get_by_id(weight_id)
        if record is None:
            raise EntityNotFoundError(f"Registro de peso com ID {weight_id} não encontrado.")
        return record

    def create(self, data: CattleWeightCreate) -> CattleWeight:
        if self._cattle_repo.get_by_id(data.cattle_id) is None:
            raise EntityNotFoundError(f"Gado com ID {data.cattle_id} não encontrado.")
        instance = CattleWeight(**data.model_dump())
        return self._repo.create(instance)

    def update(self, weight_id: int, data: CattleWeightUpdate) -> CattleWeight:
        record = self.get_by_id(weight_id)
        return self._repo.update(record, data.model_dump(exclude_unset=True))
