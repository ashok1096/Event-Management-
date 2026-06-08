"""Event repository — all DB queries for the Event model live here."""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.event_model import Event
from app.models.registration_model import Registration
from app.models.session_model import Session as SessionModel
from app.repositories.base_repository import BaseRepository


class EventRepository(BaseRepository[Event]):

    def __init__(self, db: Session):
        super().__init__(Event, db)

    def get_active_events(self, skip: int = 0, limit: int = 10) -> List[Event]:
        return (
            self.db.query(Event)
            .filter(Event.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_event_stats(self, event_id: int) -> Optional[dict]:
        event = self.get_by_id(event_id)
        if not event:
            return None

        total_registrations = (
            self.db.query(func.count(Registration.id))
            .filter(Registration.event_id == event_id)
            .scalar() or 0
        )
        total_checked_in = (
            self.db.query(func.count(Registration.id))
            .filter(Registration.event_id == event_id, Registration.is_checked_in == True)
            .scalar() or 0
        )
        total_sessions = (
            self.db.query(func.count(SessionModel.id))
            .filter(SessionModel.event_id == event_id)
            .scalar() or 0
        )

        return {
            "event_id": event.id,
            "title": event.title,
            "total_registrations": total_registrations,
            "total_checked_in": total_checked_in,
            "max_capacity": event.max_attendees,
            "capacity_remaining": (
                event.max_attendees - total_registrations if event.max_attendees else None
            ),
            "occupancy_rate": (
                round(total_registrations / event.max_attendees * 100, 2)
                if event.max_attendees else 0
            ),
            "checkin_rate": (
                round(total_checked_in / total_registrations * 100, 2)
                if total_registrations > 0 else 0
            ),
            "total_sessions": total_sessions,
            "status": event.status,
        }
