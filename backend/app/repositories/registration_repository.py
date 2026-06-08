"""Registration repository — all DB queries for the Registration model."""

import random
import string
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.registration_model import Registration
from app.models.event_model import Event
from app.repositories.base_repository import BaseRepository


class RegistrationRepository(BaseRepository[Registration]):

    def __init__(self, db: Session):
        super().__init__(Registration, db)

    def get_by_code(self, code: str) -> Optional[Registration]:
        return self.db.query(Registration).filter(Registration.registration_code == code).first()

    def get_by_event(self, event_id: int, skip: int = 0, limit: int = 10) -> List[Registration]:
        return (
            self.db.query(Registration)
            .filter(Registration.event_id == event_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_email(self, email: str) -> List[Registration]:
        return self.db.query(Registration).filter(Registration.attendee_email == email).all()

    def generate_unique_code(self, length: int = 8) -> str:
        """Loop until a registration code with no DB collision is found."""
        while True:
            code = "".join(random.choices(string.ascii_uppercase + string.digits, k=length))
            if not self.get_by_code(code):
                return code

    def get_event_stats(self, event_id: int) -> dict:
        total = (
            self.db.query(func.count(Registration.id))
            .filter(Registration.event_id == event_id)
            .scalar() or 0
        )
        checked_in = (
            self.db.query(func.count(Registration.id))
            .filter(Registration.event_id == event_id, Registration.is_checked_in == True)
            .scalar() or 0
        )
        return {
            "event_id": event_id,
            "total_registrations": total,
            "checked_in_count": checked_in,
            "checked_in_rate": round(checked_in / total * 100, 2) if total > 0 else 0,
        }
