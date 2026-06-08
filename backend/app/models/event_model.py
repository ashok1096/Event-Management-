"""Event model for SQLAlchemy ORM."""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database.postgres import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    location = Column(String(255))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    max_attendees = Column(Integer)
    current_attendees = Column(Integer, default=0)
    status = Column(String(50), default="upcoming")  # upcoming, ongoing, completed, cancelled
    organizer = Column(String(255))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)

    # Relationships
    sessions = relationship("Session", back_populates="event", cascade="all, delete-orphan")
    registrations = relationship("Registration", back_populates="event", cascade="all, delete-orphan")
    # NOTE: feedback_list relationship removed - Feedback is a Beanie (MongoDB) document
    # and cannot be related via SQLAlchemy ORM.
