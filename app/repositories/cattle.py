from sqlalchemy import extract, func

from app.models.cattle import Cattle, GenderEnum
from app.repositories.base import BaseRepository


class CattleRepository(BaseRepository[Cattle]):
    model = Cattle

    def female_has_calves(self, cattle_id: int) -> bool:
        return self.db.query(Cattle.id).filter(Cattle.mother_id == cattle_id).first() is not None

    def count(self) -> int:
        return self.db.query(func.count(Cattle.id)).scalar()

    def count_births_by_month(self, year: int) -> list[tuple[int, GenderEnum, int]]:
        return (
            self.db.query(
                extract("month", Cattle.birth_date).label("month"),
                Cattle.gender,
                func.count(Cattle.id).label("count"),
            )
            .filter(
                Cattle.birth_date.isnot(None),
                extract("year", Cattle.birth_date) == year,
            )
            .group_by("month", Cattle.gender)
            .order_by("month")
            .all()
        )
