import datetime

from sqlalchemy import Column, Integer, DECIMAL, String, Date, ForeignKey

from app.database.db import Base


class CattleWeight(Base):
    __tablename__ = "cattle_weight"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cattle_id = Column(Integer, ForeignKey("cattle.id", ondelete="CASCADE"), nullable=False)
    weight = Column(DECIMAL(10, 2), nullable=False)
    measurement_date = Column(Date, nullable=False)
    notes = Column(String, nullable=True)
    created_at = Column(Date, default=datetime.date.today, nullable=False)
    updated_at = Column(Date, onupdate=datetime.date.today, nullable=True)