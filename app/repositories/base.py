from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from app.database.db import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    model: type[T]

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, record_id: int) -> T | None:
        return self.db.query(self.model).filter(self.model.id == record_id).first()

    def get_all(self, skip: int = 0, limit: int = 9999) -> list[T]:
        return self.db.query(self.model).order_by(self.model.id).offset(skip).limit(limit).all()

    def create(self, instance: T) -> T:
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def update(self, instance: T, data: dict) -> T:
        for key, value in data.items():
            setattr(instance, key, value)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def delete(self, instance: T) -> None:
        self.db.delete(instance)
        self.db.commit()
