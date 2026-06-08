"""Check-in router - endpoints for event and session check-ins."""

from fastapi import APIRouter, Depends, HTTPException, status, Body
from app.auth.dependencies import require_role
from app.models.role_enum import Role
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import datetime, timezone
from app.database.postgres import get_db
from app.models.registration_model import Registration
from app.models.checkin_model import CheckIn
from app.models.session_model import Session as SessionModel
from app.models.event_model import Event

router = APIRouter(prefix="/checkins", tags=["checkins"])


@router.post("/registration-checkin")
async def checkin_registration(
    registration_code: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role([Role.ATTENDEE, Role.ORGANIZER, Role.ADMIN]))
):
    """Check in a registration using registration code."""
    # Find registration by code
    registration = db.query(Registration).filter(
        Registration.registration_code == registration_code
    ).first()
    
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid registration code"
        )
    
    if registration.is_checked_in:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration already checked in"
        )
    
    registration.is_checked_in = True
    registration.checked_in_at = datetime.now(timezone.utc)
    registration.status = "checked_in"
    
    # Create check-in record
    checkin = CheckIn(
        registration_id=registration.id,
        checkin_type="registration",
        timestamp=datetime.now(timezone.utc)
    )
    
    db.add(registration)
    db.add(checkin)
    db.commit()
    db.refresh(registration)
    
    return {
        "message": "Registration checked in successfully",
        "registration_id": registration.id,
        "attendee_name": registration.attendee_name,
        "checked_in_at": registration.checked_in_at.isoformat()
    }


@router.post("/session-checkin")
async def checkin_session(
    registration_id: int = Body(...),
    session_id: int = Body(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role([Role.ATTENDEE, Role.ORGANIZER, Role.ADMIN]))
):
    """Check in an attendee to a session."""
    # Validate registration exists
    registration = db.query(Registration).filter(
        Registration.id == registration_id
    ).first()
    
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )
    
    # Validate session exists
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # Check if already checked in to this session
    existing_checkin = db.query(CheckIn).filter(
        CheckIn.registration_id == registration_id,
        CheckIn.session_id == session_id
    ).first()
    
    if existing_checkin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already checked in to this session"
        )
    
    # Create check-in record
    checkin = CheckIn(
        registration_id=registration_id,
        session_id=session_id,
        checkin_type="session",
        timestamp=datetime.now(timezone.utc)
    )
    
    # Update session attendee count
    session.current_attendees += 1
    
    db.add(checkin)
    db.add(session)
    db.commit()
    db.refresh(checkin)
    
    return {
        "message": "Session check-in successful",
        "registration_id": registration_id,
        "session_id": session_id,
        "checked_in_at": checkin.timestamp.isoformat()
    }


@router.post("/session-code-checkin")
async def checkin_session_with_code(
    session_code: str = Body(...),
    registration_code: str = Body(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role([Role.ATTENDEE, Role.ORGANIZER, Role.ADMIN]))
):
    """Check in using session code and registration code."""
    # Find session by code
    session = db.query(SessionModel).filter(
        SessionModel.session_code == session_code
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid session code"
        )
    
    # Find registration by code
    registration = db.query(Registration).filter(
        Registration.registration_code == registration_code
    ).first()
    
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid registration code"
        )
    
    # Verify registration is for the event this session belongs to
    if registration.event_id != session.event_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration is not for this event"
        )
    
    # Check if already checked in to this session
    existing_checkin = db.query(CheckIn).filter(
        CheckIn.registration_id == registration.id,
        CheckIn.session_id == session.id
    ).first()
    
    if existing_checkin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already checked in to this session"
        )
    
    # Create check-in record
    checkin = CheckIn(
        registration_id=registration.id,
        session_id=session.id,
        checkin_type="session",
        timestamp=datetime.now(timezone.utc)
    )
    
    # Update session attendee count
    session.current_attendees += 1
    
    db.add(checkin)
    db.add(session)
    db.commit()
    db.refresh(checkin)
    
    return {
        "message": "Check-in successful via code",
        "session_code": session_code,
        "registration_code": registration_code,
        "checked_in_at": checkin.timestamp.isoformat()
    }


@router.get("/event/{event_id}/stats")
async def get_event_checkin_stats(event_id: int, db: Session = Depends(get_db), current_user: dict = Depends(require_role([Role.ADMIN, Role.ORGANIZER]))):
    """Get check-in statistics for an event."""
    # Verify event exists
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Get total registrations for this event
    total_registrations = db.query(func.count(Registration.id)).filter(
        Registration.event_id == event_id
    ).scalar() or 0
    
    # Get checked-in count
    total_checked_in = db.query(func.count(Registration.id)).filter(
        Registration.event_id == event_id,
        Registration.is_checked_in == True
    ).scalar() or 0
    
    checkin_rate = (
        (total_checked_in / total_registrations * 100)
        if total_registrations > 0
        else 0
    )
    
    return {
        "event_id": event_id,
        "total_registrations": total_registrations,
        "total_checked_in": total_checked_in,
        "checkin_rate": round(checkin_rate, 2)
    }


@router.get("/session/{session_id}/stats")
async def get_session_checkin_stats(session_id: int, db: Session = Depends(get_db), current_user: dict = Depends(require_role([Role.ADMIN, Role.ORGANIZER]))):
    """Get check-in statistics for a session."""
    # Verify session exists
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # Get total check-ins for this session
    total_checked_in = db.query(func.count(CheckIn.id)).filter(
        CheckIn.session_id == session_id
    ).scalar() or 0
    
    # Get registered count (registrations for the event)
    total_registered = db.query(func.count(Registration.id)).filter(
        Registration.event_id == session.event_id
    ).scalar() or 0
    
    checkin_rate = (
        (total_checked_in / total_registered * 100)
        if total_registered > 0
        else 0
    )
    
    return {
        "session_id": session_id,
        "total_registered": total_registered,
        "checked_in": total_checked_in,
        "checkin_rate": round(checkin_rate, 2)
    }
