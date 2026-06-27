import datetime

from app.models.cattle_reproduction import CattleReproduction
from app.repositories.base import BaseRepository


class CattleReproductionRepository(BaseRepository[CattleReproduction]):
    model = CattleReproduction

    def get_all(self, skip: int = 0, limit: int = 9999) -> list[CattleReproduction]:
        return (
            self.db.query(CattleReproduction)
            .filter(CattleReproduction.deleted_at.is_(None))
            .order_by(CattleReproduction.event_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_all_by_cattle(self, cattle_id: int) -> list[CattleReproduction]:
        return (
            self.db.query(CattleReproduction)
            .filter(
                CattleReproduction.cattle_id == cattle_id,
                CattleReproduction.deleted_at.is_(None),
            )
            .order_by(CattleReproduction.event_date.desc())
            .all()
        )

    def get_timeline_by_cattle(self, cattle_id: int) -> list[CattleReproduction]:
        return (
            self.db.query(CattleReproduction)
            .filter(
                CattleReproduction.cattle_id == cattle_id,
                CattleReproduction.deleted_at.is_(None),
            )
            .order_by(CattleReproduction.event_date.asc())
            .all()
        )

    def soft_delete_by_cattle(self, cattle_id: int) -> None:
        self.db.query(CattleReproduction).filter(
            CattleReproduction.cattle_id == cattle_id,
            CattleReproduction.deleted_at.is_(None),
        ).update({"deleted_at": datetime.date.today()})
        self.db.commit()
