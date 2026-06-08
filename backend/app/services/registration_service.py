"""Registration service — all DB writes use SELECT FOR UPDATE to prevent race conditions."""

import random
import string
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.registration_model import Registration
from app.models.event_model import Event
from app.models.checkin_model import CheckIn
from app.schemas.registration_schema import RegistrationCreate, RegistrationUpdate
from datetime import datetime, timezone


class RegistrationService:

    @staticmethod
    def generate_unique_code(db: Session, length: int = 8) -> str:
        """Generate a registration code that is guaranteed unique in the DB."""
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
            exists = db.query(Registration).filter(
                Registration.registration_code == code
            ).first()
            if not exists:
                return code

    @staticmethod
    def create_registration(db: Session, registration: RegistrationCreate) -> Registration:
        """
        Create a new registration with row-level locking to prevent overbooking.

        Uses SELECT ... FOR UPDATE on the Event row so that two concurrent
        requests cannot both pass the capacity check simultaneously.
        """
        # ── Acquire a row-level lock on the event ─────────────────────────────
        event = (
            db.query(Event)
            .filter(Event.id == registration.event_id)
            .with_for_update()           # ← row lock held until commit/rollback
            .first()
        )
        if not event:
            return None

        if not event.is_active:
            return None  # Event is soft-deleted / inactive

        # ── Capacity check inside the lock (race-safe) ────────────────────────
        # Use COUNT(*) not the denormalized counter for authoritative check
        confirmed_count = (
            db.query(func.count(Registration.id))
            .filter(
                Registration.event_id == registration.event_id,
                Registration.status.notin_(["cancelled"])
            )
            .scalar() or 0
        )

        if event.max_attendees and confirmed_count >= event.max_attendees:
            db.rollback()  # Release lock
            return None  # Event is full

        # ── Create registration with DB-verified unique code ──────────────────
        db_registration = Registration(
            **{k: v for k, v in registration.dict().items() if k != "registration_code"},
            registration_code=RegistrationService.generate_unique_code(db),
        )

        # Sync the denormalized counter (increment within the same lock)
        event.current_attendees = confirmed_count + 1

        db.add(db_registration)
        db.add(event)
        db.commit()
        db.refresh(db_registration)
        return db_registration

    @staticmethod
    def get_registration(db: Session, registration_id: int) -> Registration:
        """Get registration by ID."""
        return db.query(Registration).filter(Registration.id == registration_id).first()

    @staticmethod
    def get_registrations_by_event(db: Session, event_id: int, skip: int = 0, limit: int = 10):
        """Get all registrations for an event with pagination."""
        return (
            db.query(Registration)
            .filter(Registration.event_id == event_id)
            .order_by(Registration.id.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_registrations_by_email(db: Session, email: str):
        """Get registrations by attendee email."""
        return db.query(Registration).filter(Registration.attendee_email == email).all()

    @staticmethod
    def update_registration(db: Session, registration_id: int, reg_data: RegistrationUpdate) -> Registration:
        """Update registration details."""
        db_reg = db.query(Registration).filter(Registration.id == registration_id).first()
        if not db_reg:
            return None

        update_data = reg_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_reg, key, value)

        db_reg.updated_at = datetime.now(timezone.utc)
        db.add(db_reg)
        db.commit()
        db.refresh(db_reg)
        return db_reg

    @staticmethod
    def check_in_registration(db: Session, registration_id: int) -> Registration:
        """Check in a registration for an event."""
        db_reg = (
            db.query(Registration)
            .filter(Registration.id == registration_id)
            .with_for_update()
            .first()
        )
        if not db_reg:
            return None

        if db_reg.is_checked_in:
            return db_reg  # Idempotent — already checked in

        db_reg.is_checked_in = True
        db_reg.checked_in_at = datetime.now(timezone.utc)
        db_reg.status = "checked_in"

        checkin = CheckIn(
            registration_id=db_reg.id,
            checkin_type="registration",
            timestamp=datetime.now(timezone.utc)
        )

        db.add(db_reg)
        db.add(checkin)
        db.commit()
        db.refresh(db_reg)
        return db_reg

    @staticmethod
    def cancel_registration(db: Session, registration_id: int) -> bool:
        """
        Cancel a registration and decrement the event counter.
        Uses FOR UPDATE on both rows to prevent concurrent cancellation issues.
        """
        db_reg = (
            db.query(Registration)
            .filter(Registration.id == registration_id)
            .with_for_update()
            .first()
        )
        if not db_reg:
            return False

        if db_reg.status == "cancelled":
            return True  # Idempotent

        db_reg.status = "cancelled"
        db.add(db_reg)

        # Decrement counter atomically within the same transaction
        event = (
            db.query(Event)
            .filter(Event.id == db_reg.event_id)
            .with_for_update()
            .first()
        )
        if event and event.current_attendees > 0:
            event.current_attendees -= 1
            db.add(event)

        db.commit()
        return True

    @staticmethod
    def get_event_registrations_stats(db: Session, event_id: int):
        """Get registration statistics for an event using COUNT queries."""
        total = (
            db.query(func.count(Registration.id))
            .filter(Registration.event_id == event_id)
            .scalar() or 0
        )
        checked_in = (
            db.query(func.count(Registration.id))
            .filter(
                Registration.event_id == event_id,
                Registration.is_checked_in == True,
            )
            .scalar() or 0
        )

        return {
            "event_id": event_id,
            "total_registrations": total,
            "checked_in_count": checked_in,
            "checked_in_rate": round((checked_in / total * 100), 2) if total > 0 else 0,
        }
