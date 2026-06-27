import datetime

from sqlalchemy.orm import Session

from app.domain.cattle_domain import CattleDomain
from app.exceptions import EntityNotFoundError
from app.models.cattle import GenderEnum
from app.models.cattle_reproduction import CattleReproduction, ReproductiveEventEnum
from app.repositories.cattle import CattleRepository
from app.repositories.cattle_reproduction import CattleReproductionRepository
from app.schemas.cattle import BirthCreate
from app.schemas.cattle_reproduction import CattleReproductionCreate, CattleReproductionUpdate


class CattleReproductionDomain:
    def __init__(self, db: Session):
        self._repo = CattleReproductionRepository(db)
        self._cattle_repo = CattleRepository(db)
        self._cattle_domain = CattleDomain(db)

    def get_all(self, cattle_id: int | None = None) -> list[CattleReproduction]:
        if cattle_id is not None:
            return self._repo.get_all_by_cattle(cattle_id)
        return self._repo.get_all()

    def get_timeline(self, cattle_id: int) -> list[CattleReproduction]:
        return self._repo.get_timeline_by_cattle(cattle_id)

    def get_by_id(self, repro_id: int) -> CattleReproduction:
        record = self._repo.get_by_id(repro_id)
        if record is None:
            raise EntityNotFoundError(f"Registro reprodutivo com ID {repro_id} não encontrado.")
        return record

    def create(self, data: CattleReproductionCreate) -> CattleReproduction:
        mother = self._cattle_repo.get_by_id(data.cattle_id)
        if mother is None:
            raise EntityNotFoundError(f"Animal com ID {data.cattle_id} não encontrado.")

        if mother.gender != GenderEnum.FEMALE:
            raise ValueError("Eventos reprodutivos só podem ser registrados para animais fêmeas.")

        if data.partner_id and self._cattle_repo.get_by_id(data.partner_id) is None:
            raise EntityNotFoundError(f"Touro com ID {data.partner_id} não encontrado.")

        offspring_id = data.offspring_id

        if data.event_type == ReproductiveEventEnum.BIRTH:
            if data.event_date > datetime.date.today():
                raise ValueError("A data do parto não pode ser no futuro.")

            if mother.birth_date:
                age_months = (
                    (data.event_date.year - mother.birth_date.year) * 12
                    + (data.event_date.month - mother.birth_date.month)
                )
                if data.event_date.day < mother.birth_date.day:
                    age_months -= 1
                if age_months < 12:
                    raise ValueError(
                        f"A mãe tem {age_months} mês(es) na data do parto. "
                        "A idade mínima para o parto é de 12 meses."
                    )

            if not data.calf_name or not data.calf_gender:
                raise ValueError("Nome e sexo do bezerro são obrigatórios para eventos de Parto.")
            birth_data = BirthCreate(
                name=data.calf_name,
                gender=data.calf_gender,
                birth_date=data.event_date,
                mother_id=data.cattle_id,
                father_id=data.partner_id,
                identification=data.calf_identification,
                notes=data.notes,
            )
            calf = self._cattle_domain.create_birth(birth_data)
            offspring_id = calf.id

        if (
            data.event_type == ReproductiveEventEnum.PREGNANCY_CHECK
            and data.pregnancy_confirmed
            and not data.expected_birth_date
        ):
            raise ValueError("Data prevista do parto é obrigatória quando a prenhez é confirmada.")

        instance = CattleReproduction(
            cattle_id=data.cattle_id,
            event_type=data.event_type,
            event_date=data.event_date,
            partner_id=data.partner_id,
            offspring_id=offspring_id,
            pregnancy_confirmed=data.pregnancy_confirmed,
            expected_birth_date=data.expected_birth_date,
            notes=data.notes,
        )
        return self._repo.create(instance)

    def update(self, repro_id: int, data: CattleReproductionUpdate) -> CattleReproduction:
        record = self.get_by_id(repro_id)
        return self._repo.update(record, data.model_dump(exclude_unset=True))

    def delete(self, repro_id: int) -> None:
        record = self.get_by_id(repro_id)
        self._repo.delete(record)
