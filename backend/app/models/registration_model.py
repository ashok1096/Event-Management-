"""Registration model for SQLAlchemy ORM."""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from app.database.postgres import Base


class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False, index=True)
    # user_id links registration to the authenticated user account (spec: UNIQUE per user+event)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    attendee_name = Column(String(255), nullable=False)
    attendee_email = Column(String(255), nullable=False, index=True)
    phone = Column(String(20))
    company = Column(String(255))
    designation = Column(String(255))
    registration_code = Column(String(20), unique=True, index=True)  # Code for check-in
    status = Column(String(50), default="registered")  # registered, checked_in, cancelled
    is_checked_in = Column(Boolean, default=False)
    checked_in_at = Column(DateTime)
    payment_status = Column(String(50), default="pending")  # pending, completed, failed
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    event = relationship("Event", back_populates="registrations")
    checkins = relationship("CheckIn", back_populates="registration", cascade="all, delete-orphan")

    # Constraints
    __table_args__ = (
        # Spec: UNIQUE(user_id, event_id) — one registration per authenticated user per event
        UniqueConstraint("user_id", "event_id", name="uq_user_event_registration"),
        # Prevent guest duplicate registrations: same email cannot register for same event twice
        UniqueConstraint("event_id", "attendee_email", name="uq_event_email_registration"),
        Index("idx_attendee_email", "attendee_email"),
        Index("idx_registration_status", "status"),
        Index("idx_registration_user_id", "user_id"),
    )
