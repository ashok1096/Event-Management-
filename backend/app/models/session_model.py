"""Session model for SQLAlchemy ORM."""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Index
from sqlalchemy.orm import relationship
from app.database.postgres import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    speaker_id = Column(Integer, ForeignKey("speakers.id"), index=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    location = Column(String(255))
    capacity = Column(Integer)
    current_attendees = Column(Integer, default=0)
    session_code = Column(String(20), unique=True, index=True)  # Code-based attendance
    status = Column(String(50), default="scheduled")  # scheduled, ongoing, completed, cancelled
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    event = relationship("Event", back_populates="sessions")
    speaker = relationship("Speaker", back_populates="sessions")
    checkins = relationship("CheckIn", back_populates="session", cascade="all, delete-orphan")

    # Indexes for efficient queries
    __table_args__ = (
        Index('idx_session_event_id', 'event_id'),
        Index('idx_session_speaker_id', 'speaker_id'),
        Index('idx_session_status', 'status'),
        Index('idx_session_start_time', 'start_time'),
    )
