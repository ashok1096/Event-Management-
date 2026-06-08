"""Speakers router - endpoints for speaker management."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.postgres import get_db
from app.schemas.speaker_schema import SpeakerSchema, SpeakerCreate, SpeakerUpdate, SpeakerListResponse
from app.services.speaker_service import SpeakerService
from app.auth.dependencies import require_role
from app.models.role_enum import Role

router = APIRouter(prefix="/speakers", tags=["speakers"])


@router.post("/", response_model=SpeakerSchema, status_code=status.HTTP_201_CREATED)
async def create_speaker(speaker: SpeakerCreate, db: Session = Depends(get_db), current_user: dict = Depends(require_role([Role.ADMIN, Role.ORGANIZER]))):
    """Create a new speaker."""
    # Check if speaker already exists
    existing = SpeakerService.get_speaker_by_email(db, speaker.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Speaker with this email already exists"
        )

    db_speaker = SpeakerService.create_speaker(db, speaker)
    return db_speaker


@router.get("/{speaker_id}", response_model=SpeakerSchema)
async def get_speaker(speaker_id: int, db: Session = Depends(get_db)):
    """Get speaker by ID."""
    speaker = SpeakerService.get_speaker(db, speaker_id)
    if not speaker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Speaker not found"
        )
    return speaker


@router.get("/", response_model=List[SpeakerListResponse])
async def list_speakers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Get all speakers with session count per speaker."""
    return SpeakerService.get_all_speakers(db, skip=skip, limit=limit)


@router.put("/{speaker_id}", response_model=SpeakerSchema)
async def update_speaker(speaker_id: int, speaker: SpeakerUpdate, db: Session = Depends(get_db), current_user: dict = Depends(require_role([Role.ADMIN, Role.ORGANIZER]))):
    """Update speaker details."""
    db_speaker = SpeakerService.update_speaker(db, speaker_id, speaker)
    if not db_speaker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Speaker not found"
        )
    return db_speaker


@router.delete("/{speaker_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_speaker(speaker_id: int, db: Session = Depends(get_db), current_user: dict = Depends(require_role([Role.ADMIN, Role.ORGANIZER]))):
    """Delete (soft delete) a speaker."""
    success = SpeakerService.delete_speaker(db, speaker_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Speaker not found"
        )
    return None


@router.get("/{speaker_id}/sessions")
async def get_speaker_sessions(speaker_id: int, db: Session = Depends(get_db)):
    """Get all sessions for a speaker."""
    sessions = SpeakerService.get_speaker_sessions(db, speaker_id)
    if not sessions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Speaker not found"
        )
    return sessions
