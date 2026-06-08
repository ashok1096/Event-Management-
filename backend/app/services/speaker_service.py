"""Speaker service for business logic."""

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.speaker_model import Speaker
from app.models.session_model import Session as SessionModel
from app.schemas.speaker_schema import SpeakerCreate, SpeakerUpdate
from datetime import datetime, timezone


class SpeakerService:
    @staticmethod
    def create_speaker(db: Session, speaker: SpeakerCreate) -> Speaker:
        """Create a new speaker."""
        db_speaker = Speaker(**speaker.dict())
        db.add(db_speaker)
        db.commit()
        db.refresh(db_speaker)
        return db_speaker

    @staticmethod
    def get_speaker(db: Session, speaker_id: int) -> Speaker:
        """Get speaker by ID."""
        return db.query(Speaker).filter(Speaker.id == speaker_id).first()

    @staticmethod
    def get_speaker_by_email(db: Session, email: str) -> Speaker:
        """Get speaker by email."""
        return db.query(Speaker).filter(Speaker.email == email).first()

    @staticmethod
    def get_all_speakers(db: Session, skip: int = 0, limit: int = 10):
        """Get all active speakers with session count per speaker using COUNT query."""
        results = (
            db.query(
                Speaker,
                func.count(SessionModel.id).label("sessions_count")
            )
            .outerjoin(SessionModel, SessionModel.speaker_id == Speaker.id)
            .filter(Speaker.is_active == True)
            .group_by(Speaker.id)
            .order_by(Speaker.id.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        speakers_with_count = []
        for speaker, sessions_count in results:
            speaker_dict = {
                "id": speaker.id,
                "name": speaker.name,
                "email": speaker.email,
                "bio": speaker.bio,
                "company": speaker.company,
                "expertise": speaker.expertise,
                "profile_url": speaker.profile_url,
                "sessions_count": sessions_count,
                "created_at": speaker.created_at,
                "updated_at": speaker.updated_at,
            }
            speakers_with_count.append(speaker_dict)

        return speakers_with_count

    @staticmethod
    def update_speaker(db: Session, speaker_id: int, speaker_data: SpeakerUpdate) -> Speaker:
        """Update speaker details."""
        db_speaker = db.query(Speaker).filter(Speaker.id == speaker_id).first()
        if not db_speaker:
            return None

        update_data = speaker_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_speaker, key, value)

        db_speaker.updated_at = datetime.now(timezone.utc)
        db.add(db_speaker)
        db.commit()
        db.refresh(db_speaker)
        return db_speaker

    @staticmethod
    def delete_speaker(db: Session, speaker_id: int) -> bool:
        """Soft delete speaker."""
        db_speaker = db.query(Speaker).filter(Speaker.id == speaker_id).first()
        if not db_speaker:
            return False

        db_speaker.is_active = False
        db.add(db_speaker)
        db.commit()
        return True

    @staticmethod
    def get_speaker_sessions(db: Session, speaker_id: int):
        """Get all sessions for a speaker."""
        speaker = db.query(Speaker).filter(Speaker.id == speaker_id).first()
        if not speaker:
            return None

        sessions_count = db.query(func.count(SessionModel.id)).filter(
            SessionModel.speaker_id == speaker_id
        ).scalar() or 0

        return {
            "speaker_id": speaker.id,
            "name": speaker.name,
            "email": speaker.email,
            "bio": speaker.bio,
            "sessions_count": sessions_count,
            "sessions": [
                {"id": s.id, "title": s.title, "event_id": s.event_id}
                for s in speaker.sessions
            ]
        }
