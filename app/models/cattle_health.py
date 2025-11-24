import datetime

from sqlalchemy import Column, Integer, DECIMAL, String, Date, ForeignKey, Enum

from app.database.db import Base

import enum

class HealthRecordTypeEnum(str, enum.Enum):
    VACCINATION = "VACCINATION"
    DISEASE = "DISEASE"
    INJURY = "INJURY"
    TREATMENT = "TREATMENT"
    CHECKUP = "CHECKUP"

class CattleHealth(Base):
    __tablename__ = "cattle_health"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cattle_id = Column(Integer, ForeignKey("cattle.id", ondelete="CASCADE"), nullable=False)
    record_type = Column(Enum(HealthRecordTypeEnum, name="health_record_type_enum"), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String, nullable=False)  # nome da vacina, doença, etc
    veterinarian = Column(String, nullable=True)
    medication = Column(String, nullable=True)
    dosage = Column(String, nullable=True)
    cost = Column(DECIMAL(10, 2), nullable=True)
    next_dose_date = Column(Date, nullable=True)  # para reforços de vacina
    notes = Column(String, nullable=True)
    created_at = Column(Date, default=datetime.date.today, nullable=False)
    updated_at = Column(Date, onupdate=datetime.date.today, nullable=True)