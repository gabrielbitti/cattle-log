from sqlalchemy import Column, Integer, String, DECIMAL, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db import Base
import datetime

class Cattle(Base):
    __tablename__ = "cattle"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    weight = Column(DECIMAL(10,2), nullable=True)
    birth_date = Column(Date, nullable=True)
    created_at = Column(Date, default=datetime.datetime.now(), nullable=True)
    updated_at = Column(Date, nullable=True)
    name = Column(String, nullable=False)
    type = Column(String, index=True, nullable=False) # e.g., \'cow\', \'bull\'
    mother_id = Column(Integer, ForeignKey("cattle.id"), nullable=True)

    mother = relationship("Cattle", remote_side=[id], back_populates="calves")
    calves = relationship("Cattle", back_populates="mother")

    # Ensure type is either \'cow\' or \'bull\'
    # __table_args__ = (CheckConstraint(type.in_([\'cow\', \'bull\'])),)
    # Note: CheckConstraint might need specific import and handling depending on DB
