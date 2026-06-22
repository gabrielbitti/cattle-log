from app.models.cattle_weight import CattleWeight
from app.repositories.base import BaseRepository


class CattleWeightRepository(BaseRepository[CattleWeight]):
    model = CattleWeight

    def get_all_by_cattle(self, cattle_id: int) -> list[CattleWeight]:
        return (
            self.db.query(CattleWeight)
            .filter(CattleWeight.cattle_id == cattle_id)
            .order_by(CattleWeight.id)
            .all()
        )
