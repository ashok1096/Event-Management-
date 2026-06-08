"""Events router - endpoints for event management."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.postgres import get_db
from app.schemas.event_schema import EventSchema, EventCreate, EventUpdate
from app.services.event_service import EventService
from app.auth.dependencies import require_role
from app.models.role_enum import Role

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/", response_model=List[EventSchema])
async def list_events(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Get all active events with pagination. Public endpoint."""
    return EventService.get_all_events(db, skip=skip, limit=limit)


@router.get("/{event_id}", response_model=EventSchema)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get event by ID. Public endpoint."""
    event = EventService.get_event(db, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return event


@router.post("/", response_model=EventSchema, status_code=status.HTTP_201_CREATED)
async def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role([Role.ORGANIZER, Role.ADMIN]))
):
    """Create a new event. Requires Organizer or Admin role."""
    db_event = EventService.create_event(db, event)
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create event"
        )
    return db_event


@router.put("/{event_id}", response_model=EventSchema)
async def update_event(
    event_id: int,
    event: EventUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role([Role.ORGANIZER, Role.ADMIN]))
):
    """Update event details. Requires Organizer or Admin role."""
    db_event = EventService.update_event(db, event_id, event)
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return db_event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role([Role.ORGANIZER, Role.ADMIN]))
):
    """Soft delete an event. Requires Organizer or Admin role."""
    success = EventService.delete_event(db, event_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return None


@router.get("/{event_id}/stats")
async def get_event_stats(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role([Role.ORGANIZER, Role.ADMIN]))
):
    """Get event statistics. Requires Organizer or Admin role."""
    stats = EventService.get_event_stats(db, event_id)
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return stats
