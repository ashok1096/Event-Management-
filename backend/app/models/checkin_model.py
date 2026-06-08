"""Check-in model for SQLAlchemy ORM."""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from app.database.postgres import Base


class CheckIn(Base):
    __tablename__ = "checkins"

    id = Column(Integer, primary_key=True, index=True)
    registration_id = Column(Integer, ForeignKey("registrations.id"), nullable=False, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=True, index=True)
    checkin_type = Column(String(50), default="session")  # registration, session
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    location = Column(String(255))
    device_id = Column(String(100))  # For tracking which device performed check-in

    # Relationships
    registration = relationship("Registration", back_populates="checkins")
    session = relationship("Session", back_populates="checkins")

    # Constraints
    __table_args__ = (
        # Prevent duplicate check-ins for the same registration+session pair
        UniqueConstraint('registration_id', 'session_id', name='uix_registration_session_checkin'),
        Index('idx_checkin_registration_id', 'registration_id'),
        Index('idx_checkin_session_id', 'session_id'),
    )
