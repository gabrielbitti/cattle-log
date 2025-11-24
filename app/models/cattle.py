import datetime

from sqlalchemy import Column, Integer, String, Date, ForeignKey

from app.database.db import Base


class Cattle(Base):
    __tablename__ = "cattle"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    birth_date = Column(Date, nullable=True)
    created_at = Column(Date, default=datetime.datetime.now(), nullable=True)
    updated_at = Column(Date, nullable=True)
    name = Column(String, nullable=False)
    type = Column(String, index=True, nullable=False)
    mother_id = Column(Integer, ForeignKey("cattle.id"), nullable=True)
