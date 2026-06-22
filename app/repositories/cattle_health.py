from app.models.cattle_health import CattleHealth
from app.repositories.base import BaseRepository


class CattleHealthRepository(BaseRepository[CattleHealth]):
    model = CattleHealth

    def get_all_by_cattle(self, cattle_id: int) -> list[CattleHealth]:
        return (
            self.db.query(CattleHealth)
            .filter(CattleHealth.cattle_id == cattle_id)
            .order_by(CattleHealth.id)
            .all()
        )
