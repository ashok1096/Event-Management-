"""Sessions router - endpoints for session management."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session as DBSession
from typing import List
import uuid

from app.database.postgres import get_db
from app.models.session_model import Session as SessionModel
from app.models.event_model import Event
from app.schemas.session_schema import SessionCreate, SessionUpdate, SessionSchema
from app.auth.dependencies import require_role
from app.models.role_enum import Role

router = APIRouter(prefix="/sessions", tags=["sessions"])



@router.get("/")
def list_sessions(skip: int = 0, limit: int = 10, db: DBSession = Depends(get_db), current_user: dict = Depends(require_role([Role.ATTENDEE, Role.ORGANIZER, Role.ADMIN]))):
    sessions = db.query(SessionModel).order_by(SessionModel.id.asc()).offset(skip).limit(limit).all()
    total = db.query(SessionModel).count()

    return {
        "sessions": sessions,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.post("/")
def create_session(session: SessionCreate, db: DBSession = Depends(get_db), current_user: dict = Depends(require_role([Role.ORGANIZER, Role.ADMIN]))):
    event = db.query(Event).filter(Event.id == session.event_id).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found. Create event first."
        )
    
    # If speaker is assigned, validate session constraints
    if session.speaker_id:
        from app.models.speaker_model import Speaker
        speaker = db.query(Speaker).filter(Speaker.id == session.speaker_id).first()
        
        if not speaker:
            raise HTTPException(
                status_code=404,
                detail="Speaker not found"
            )
        
        # Check for overlapping sessions for the same speaker
        overlapping = db.query(SessionModel).filter(
            SessionModel.speaker_id == session.speaker_id,
            SessionModel.status != "cancelled",
            # Check time overlap: new session starts before existing ends AND new session ends after existing starts
            SessionModel.start_time < session.end_time,
            SessionModel.end_time > session.start_time
        ).first()
        
        if overlapping:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Speaker {speaker.name} has an overlapping session at {overlapping.start_time.isoformat()}"
            )
        
        # Limit speaker to max 5 sessions per day
        from datetime import timedelta
        day_start = session.start_time.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        
        sessions_today = db.query(SessionModel).filter(
            SessionModel.speaker_id == session.speaker_id,
            SessionModel.status != "cancelled",
            SessionModel.start_time >= day_start,
            SessionModel.start_time < day_end
        ).count()
        
        if sessions_today >= 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Speaker {speaker.name} has reached maximum of 5 sessions per day"
            )

    new_session = SessionModel(
        event_id=session.event_id,
        title=session.title,
        description=session.description,
        speaker_id=session.speaker_id,
        start_time=session.start_time,
        end_time=session.end_time,
        location=session.location,
        capacity=session.capacity,
        session_code=str(uuid.uuid4())[:8],
        status="scheduled"
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return {
        "message": "Session created successfully",
        "session_id": new_session.id,
        "session": new_session
    }


@router.get("/{session_id}")
async def get_session(
    session_id: int,
    db: DBSession = Depends(get_db),
    current_user: dict = Depends(require_role([Role.ATTENDEE, Role.ORGANIZER, Role.ADMIN]))
):
    """Get session detail. Merges PostgreSQL session data with MongoDB speaker profile."""
    from app.models.speaker_profile_model import SpeakerProfile

    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Build base session dict
    session_dict = {
        "id": session.id,
        "event_id": session.event_id,
        "title": session.title,
        "description": session.description,
        "speaker_id": session.speaker_id,
        "start_time": session.start_time.isoformat() if session.start_time else None,
        "end_time": session.end_time.isoformat() if session.end_time else None,
        "location": session.location,
        "capacity": session.capacity,
        "current_attendees": session.current_attendees,
        "session_code": session.session_code,
        "status": session.status,
    }

    # Merge MongoDB speaker profile (bio, past_talks, social_links)
    speaker_profile = None
    if session.speaker_id:
        speaker_profile = await SpeakerProfile.find_one(
            SpeakerProfile.speaker_id == session.speaker_id
        )

    session_dict["speaker_profile"] = (
        {
            "bio": speaker_profile.bio,
            "company": speaker_profile.company,
            "expertise": speaker_profile.expertise,
            "past_talks": speaker_profile.past_talks,
            "social_links": speaker_profile.social_links,
            "photo_url": speaker_profile.photo_url,
        }
        if speaker_profile else None
    )

    return session_dict



@router.put("/{session_id}")
def update_session(
    session_id: int,
    session_data: SessionUpdate,
    db: DBSession = Depends(get_db),
    current_user: dict = Depends(require_role([Role.ORGANIZER, Role.ADMIN]))
):
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    update_data = session_data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(session, key, value)

    db.commit()
    db.refresh(session)

    return {
        "message": "Session updated successfully",
        "session": session
    }


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_id: int, db: DBSession = Depends(get_db), current_user: dict = Depends(require_role([Role.ORGANIZER, Role.ADMIN]))):
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        from sqlalchemy import text
        # Clean up any potential orphaned records in old tables if they exist
        db.execute(text("DELETE FROM checkins WHERE session_id = :id"), {"id": session_id})
        db.execute(text("DELETE FROM feedback WHERE session_id = :id"), {"id": session_id})
        db.delete(session)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    return None


@router.post("/{session_id}/start")
def start_session(session_id: int, db: DBSession = Depends(get_db), current_user: dict = Depends(require_role([Role.ORGANIZER, Role.ADMIN]))):
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session.status = "ongoing"
    db.commit()
    db.refresh(session)

    return {"session_id": session.id, "status": session.status}


@router.post("/{session_id}/end")
def end_session(session_id: int, db: DBSession = Depends(get_db), current_user: dict = Depends(require_role([Role.ORGANIZER, Role.ADMIN]))):
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session.status = "completed"
    db.commit()
    db.refresh(session)

    return {"session_id": session.id, "status": session.status}


@router.get("/{session_id}/attendance")
def get_session_attendance(session_id: int, db: DBSession = Depends(get_db)):
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "session_id": session.id,
        "attendance_count": session.current_attendees
    }