"""Event service for business logic."""

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.event_model import Event
from app.models.registration_model import Registration
from app.models.session_model import Session as SessionModel
from app.schemas.event_schema import EventCreate, EventUpdate
from datetime import datetime, timezone


class EventService:
    @staticmethod
    def create_event(db: Session, event: EventCreate) -> Event:
        """Create a new event."""
        db_event = Event(**event.dict())
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event

    @staticmethod
    def get_event(db: Session, event_id: int) -> Event:
        """Get event by ID."""
        return db.query(Event).filter(Event.id == event_id).first()

    @staticmethod
    def get_all_events(db: Session, skip: int = 0, limit: int = 10):
        """Get all active events with pagination."""
        return (
            db.query(Event)
            .filter(Event.is_active == True)
            .order_by(Event.id.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def update_event(db: Session, event_id: int, event_data: EventUpdate) -> Event:
        """Update event details."""
        db_event = db.query(Event).filter(Event.id == event_id).first()
        if not db_event:
            return None

        update_data = event_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_event, key, value)

        db_event.updated_at = datetime.now(timezone.utc)
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event

    @staticmethod
    def delete_event(db: Session, event_id: int) -> bool:
        """Soft delete event and cascade is_active=False to related sessions and registrations."""
        db_event = db.query(Event).filter(Event.id == event_id).first()
        if not db_event:
            return False

        # Soft-delete the event
        db_event.is_active = False

        # Cascade: mark all related sessions as inactive
        db.query(SessionModel).filter(SessionModel.event_id == event_id).update(
            {"is_active": False},
            synchronize_session="fetch"
        )

        # Cascade: cancel all pending registrations for this event
        db.query(Registration).filter(
            Registration.event_id == event_id,
            Registration.status == "registered"
        ).update(
            {"status": "cancelled"},
            synchronize_session="fetch"
        )

        db.add(db_event)
        db.commit()
        return True

    @staticmethod
    def get_event_stats(db: Session, event_id: int):
        """Get event statistics using COUNT queries instead of denormalized counters."""
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            return None

        # Use actual COUNT queries to ensure accuracy
        total_registrations = db.query(func.count(Registration.id)).filter(
            Registration.event_id == event_id
        ).scalar() or 0
        
        total_checked_in = db.query(func.count(Registration.id)).filter(
            Registration.event_id == event_id,
            Registration.is_checked_in == True
        ).scalar() or 0
        
        total_sessions = db.query(func.count(SessionModel.id)).filter(
            SessionModel.event_id == event_id
        ).scalar() or 0

        total_speakers = db.query(func.count(func.distinct(SessionModel.speaker_id))).filter(
            SessionModel.event_id == event_id,
            SessionModel.speaker_id.isnot(None)
        ).scalar() or 0

        return {
            "event_id": event.id,
            "title": event.title,
            "total_registrations": total_registrations,
            "total_checked_in": total_checked_in,
            "max_capacity": event.max_attendees,
            "occupancy_rate": (
                (total_registrations / event.max_attendees * 100)
                if event.max_attendees
                else 0
            ),
            "checkin_rate": (
                (total_checked_in / total_registrations * 100)
                if total_registrations > 0
                else 0
            ),
            "total_sessions": total_sessions,
            "total_speakers": total_speakers,
            "status": event.status,
            "start_date": event.start_date.isoformat() if event.start_date else None,
            "end_date": event.end_date.isoformat() if event.end_date else None
        }
