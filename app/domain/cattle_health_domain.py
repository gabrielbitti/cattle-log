from sqlalchemy.orm import Session

from app.exceptions import EntityNotFoundError
from app.models.cattle_health import CattleHealth
from app.repositories.cattle import CattleRepository
from app.repositories.cattle_health import CattleHealthRepository
from app.schemas.cattle_health import CattleHealthCreate, CattleHealthUpdate


class CattleHealthDomain:
    def __init__(self, db: Session):
        self._repo = CattleHealthRepository(db)
        self._cattle_repo = CattleRepository(db)

    def get_all(self, cattle_id: int | None = None) -> list[CattleHealth]:
        if cattle_id is not None:
            return self._repo.get_all_by_cattle(cattle_id)
        return self._repo.get_all()

    def get_by_id(self, health_id: int) -> CattleHealth:
        record = self._repo.get_by_id(health_id)
        if record is None:
            raise EntityNotFoundError(f"Registro de saúde com ID {health_id} não encontrado.")
        return record

    def create(self, data: CattleHealthCreate) -> CattleHealth:
        if self._cattle_repo.get_by_id(data.cattle_id) is None:
            raise EntityNotFoundError(f"Gado com ID {data.cattle_id} não encontrado.")
        instance = CattleHealth(**data.model_dump())
        return self._repo.create(instance)

    def update(self, health_id: int, data: CattleHealthUpdate) -> CattleHealth:
        record = self.get_by_id(health_id)
        return self._repo.update(record, data.model_dump(exclude_unset=True))
