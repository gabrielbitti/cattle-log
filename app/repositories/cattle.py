from sqlalchemy import func

from app.models.cattle import Cattle
from app.repositories.base import BaseRepository


class CattleRepository(BaseRepository[Cattle]):
    model = Cattle

    def female_has_calves(self, cattle_id: int) -> bool:
        return self.db.query(Cattle.id).filter(Cattle.mother_id == cattle_id).first() is not None

    def count(self) -> int:
        return self.db.query(func.count(Cattle.id)).scalar()
