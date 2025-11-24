import datetime
import enum

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, Enum

from app.database.db import Base


class ReproductiveEventEnum(str, enum.Enum):
    MATING = "MATING"
    PREGNANCY_CHECK = "PREGNANCY_CHECK"
    BIRTH = "BIRTH"
    ABORTION = "ABORTION"
    WEANING = "WEANING"

class CattleReproduction(Base):
    __tablename__ = "cattle_reproduction"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cattle_id = Column(Integer, ForeignKey("cattle.id", ondelete="CASCADE"), nullable=False)
    event_type = Column(Enum(ReproductiveEventEnum, name="reproductive_event_enum"), nullable=False)
    event_date = Column(Date, nullable=False)
    partner_id = Column(Integer, ForeignKey("cattle.id"), nullable=True)  # touro/vaca
    offspring_id = Column(Integer, ForeignKey("cattle.id"), nullable=True)  # cria gerada
    pregnancy_confirmed = Column(Boolean, nullable=True)
    expected_birth_date = Column(Date, nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(Date, default=datetime.date.today, nullable=False)
    updated_at = Column(Date, onupdate=datetime.date.today, nullable=True)