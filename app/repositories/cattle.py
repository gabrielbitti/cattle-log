import calendar
import datetime
from datetime import date

from sqlalchemy import extract, func, select

from app.models.cattle import Cattle, GenderEnum
from app.models.cattle_reproduction import CattleReproduction, ReproductiveEventEnum
from app.repositories.base import BaseRepository


class CattleRepository(BaseRepository[Cattle]):
    model = Cattle

    def get_by_id(self, record_id: int) -> Cattle | None:
        return (
            self.db.query(Cattle)
            .filter(Cattle.id == record_id, Cattle.deleted_at.is_(None))
            .first()
        )

    def get_all(self, skip: int = 0, limit: int = 9999) -> list[Cattle]:
        return (
            self.db.query(Cattle)
            .filter(Cattle.deleted_at.is_(None))
            .order_by(Cattle.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def female_has_calves(self, cattle_id: int) -> bool:
        return (
            self.db.query(Cattle.id)
            .filter(Cattle.mother_id == cattle_id, Cattle.deleted_at.is_(None))
            .first()
        ) is not None

    def count(self) -> int:
        return (
            self.db.query(func.count(Cattle.id))
            .filter(Cattle.deleted_at.is_(None))
            .scalar()
        )

    def count_births_by_month(self, year: int) -> list[tuple[int, GenderEnum, int]]:
        return (
            self.db.query(
                extract("month", Cattle.birth_date).label("month"),
                Cattle.gender,
                func.count(Cattle.id).label("count"),
            )
            .filter(
                Cattle.birth_date.isnot(None),
                Cattle.deleted_at.is_(None),
                extract("year", Cattle.birth_date) == year,
            )
            .group_by("month", Cattle.gender)
            .order_by("month")
            .all()
        )

    def get_pending_weanings(self) -> list[Cattle]:
        today = date.today()
        month = today.month - 7
        year = today.year
        if month <= 0:
            month += 12
            year -= 1
        max_day = calendar.monthrange(year, month)[1]
        cutoff = today.replace(year=year, month=month, day=min(today.day, max_day))

        weaned_ids = select(CattleReproduction.offspring_id).where(
            CattleReproduction.event_type == ReproductiveEventEnum.WEANING,
            CattleReproduction.offspring_id.isnot(None),
            CattleReproduction.deleted_at.is_(None),
        )
        return (
            self.db.query(Cattle)
            .filter(
                Cattle.birth_date >= cutoff,
                Cattle.birth_date.isnot(None),
                Cattle.deleted_at.is_(None),
                ~Cattle.id.in_(weaned_ids),
            )
            .order_by(Cattle.birth_date)
            .all()
        )

    def soft_delete(self, instance: Cattle) -> None:
        instance.deleted_at = datetime.date.today()
        self.db.commit()
