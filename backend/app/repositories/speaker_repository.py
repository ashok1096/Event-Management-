"""Speaker repository — all DB queries for the Speaker model live here."""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.speaker_model import Speaker
from app.models.session_model import Session as SessionModel
from app.repositories.base_repository import BaseRepository


class SpeakerRepository(BaseRepository[Speaker]):

    def __init__(self, db: Session):
        super().__init__(Speaker, db)

    def get_by_email(self, email: str) -> Optional[Speaker]:
        return self.db.query(Speaker).filter(Speaker.email == email).first()

    def get_active_speakers_with_session_count(self, skip: int = 0, limit: int = 10) -> List[dict]:
        results = (
            self.db.query(Speaker, func.count(SessionModel.id).label("sessions_count"))
            .outerjoin(SessionModel, SessionModel.speaker_id == Speaker.id)
            .filter(Speaker.is_active == True)
            .group_by(Speaker.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [
            {**{c.name: getattr(spk, c.name) for c in Speaker.__table__.columns}, "sessions_count": cnt}
            for spk, cnt in results
        ]

    def get_session_count(self, speaker_id: int) -> int:
        return (
            self.db.query(func.count(SessionModel.id))
            .filter(SessionModel.speaker_id == speaker_id)
            .scalar() or 0
        )
