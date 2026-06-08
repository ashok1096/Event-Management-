"""Speaker model for SQLAlchemy ORM."""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database.postgres import Base


class Speaker(Base):
    __tablename__ = "speakers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    bio = Column(Text)
    company = Column(String(255))
    expertise = Column(String(255))
    profile_url = Column(String(255))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)

    # Relationships
    sessions = relationship("Session", back_populates="speaker")
