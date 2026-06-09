import datetime
import enum

from sqlalchemy import Column, DECIMAL, Integer, String, Date, ForeignKey, Enum, func
from sqlalchemy.orm import relationship, Session
# from app.schemas.cattle import CattleCreate, CattleUpdate, BirthCreate
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

    # Relationships
    weight_records = relationship("CattleWeight", back_populates="cattle", lazy="select", cascade="all, delete-orphan")
    mother = relationship("Cattle", remote_side=[id], foreign_keys=[mother_id], back_populates="offspring_as_mother")
    father = relationship("Cattle", remote_side=[id], foreign_keys=[father_id], back_populates="offspring_as_father")
    offspring_as_mother = relationship("Cattle", foreign_keys=[mother_id], back_populates="mother")
    offspring_as_father = relationship("Cattle", foreign_keys=[father_id], back_populates="father")


class CattleDTO:
    """."""

    def __init__(self, db: Session):
        """."""
        self.db = db

    def get_by_id(self, cattle_id: int):
        """Fetches a single cattle record by its ID."""
        return self.db.query(Cattle).filter(Cattle.id == cattle_id).first()

    def get_all(self, skip: int = 0, limit: int = 9999):
        """Fetches a list of cattle records, ordered by ID."""
        return self.db.query(Cattle).order_by(Cattle.id).offset(skip).limit(limit).all()

    def create_cattle_in_database(self, cattle):
        """Creates a new cattle record."""
        db_cattle = Cattle(**cattle.model_dump())
        self.db.add(db_cattle)
        self.db.commit()
        self.db.refresh(db_cattle)

        return db_cattle

    def female_has_calves(self, cattle_id: int):
        """."""
        return self.db.query(Cattle.id).filter(Cattle.mother_id == cattle_id).first() is not None

    def update(self, db_cattle, update_data):
        """Updates an existing cattle record."""
        for key, value in update_data.items():
            setattr(db_cattle, key, value)

        self.db.commit()
        self.db.refresh(db_cattle)

        return db_cattle

    def create_birth(self, db_calf):
        """Registers a birth, creating a new calf linked to a mother cow."""
        # mother = self.get_by_id(birth.mother_id)
        # if not mother or mother.gender != "FEMALE":
        #     raise ValueError(
        #         f"Vaca mãe com ID {birth.mother_id} não encontrada ou não é uma fêmea.")
        #
        # # Validate father if provided
        # if birth.father_id:
        #     father = self.get_by_id(birth.father_id)
        #     if not father or father.gender != "MALE":
        #         raise ValueError(
        #             f"Pai com ID {birth.father_id} não encontrado ou não é um macho.")
        #
        # # Set default race from mother if not provided
        # calf_race = birth.race if birth.race else mother.race
        #
        # # Create the calf record
        # db_calf = Cattle(
        #     name=birth.name,
        #     race=calf_race,
        #     gender=birth.gender,
        #     birth_date=birth.birth_date,
        #     mother_id=birth.mother_id,
        #     father_id=birth.father_id,
        #     notes=birth.notes,
        #     status="ACTIVE"
        # )
        self.db.add(db_calf)
        self.db.commit()
        self.db.refresh(db_calf)

        return db_calf

    def get_cattle_count(self) -> int:
        """Counts the total number of cattle records."""
        # Using count() is generally efficient for simple counts
        return self.db.query(func.count(Cattle.id)).scalar()
