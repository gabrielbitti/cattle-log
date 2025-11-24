import datetime
import enum

from sqlalchemy import Column, DECIMAL, Integer, String, Date, ForeignKey, Enum

from app.database.db import Base


class GenderEnum(str, enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"

class StatusEnum(str, enum.Enum):
    ACTIVE = "ACTIVE"
    SOLD = "SOLD"
    DECEASED = "DECEASED"
    TRANSFERRED = "TRANSFERRED"

class Cattle(Base):
    __tablename__ = "cattle"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    identification = Column(String, unique=True, nullable=True)
    race = Column(String, index=True, nullable=False)
    gender = Column(Enum(GenderEnum, name="gender_enum"), nullable=False)
    birth_date = Column(Date, nullable=True)
    acquisition_date = Column(Date, nullable=True)
    acquisition_value = Column(DECIMAL(10, 2), nullable=True)
    status = Column(Enum(StatusEnum, name="status_enum"), default=StatusEnum.ACTIVE, nullable=False)
    mother_id = Column(Integer, ForeignKey("cattle.id"), nullable=True)
    father_id = Column(Integer, ForeignKey("cattle.id"), nullable=True)
    origin = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(Date, default=datetime.date.today, nullable=False)
    updated_at = Column(Date, onupdate=datetime.date.today, nullable=True)