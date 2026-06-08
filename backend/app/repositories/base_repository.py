"""Base repository providing generic CRUD operations.

All entity-specific repositories inherit from BaseRepository,
which keeps DB query logic out of routers and service classes.
"""

from typing import Generic, List, Optional, Type, TypeVar
from sqlalchemy.orm import Session
from app.database.postgres import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Generic CRUD repository for SQLAlchemy models."""

    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, id: int) -> Optional[ModelType]:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 10) -> List[ModelType]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, obj: ModelType) -> ModelType:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj: ModelType) -> ModelType:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: ModelType) -> None:
        self.db.delete(obj)
        self.db.commit()

    def soft_delete(self, obj: ModelType) -> ModelType:
        """Set is_active=False instead of hard deleting."""
        obj.is_active = False
        return self.update(obj)
