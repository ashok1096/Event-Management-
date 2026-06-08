"""Registrations router - endpoints for attendee registration."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.postgres import get_db
from app.schemas.registration_schema import RegistrationSchema, RegistrationCreate, RegistrationUpdate
from app.services.registration_service import RegistrationService
from app.auth.dependencies import require_role
from app.models.role_enum import Role

router = APIRouter(prefix="/registrations", tags=["registrations"])


@router.post("/", response_model=RegistrationSchema, status_code=status.HTTP_201_CREATED)
async def create_registration(
    registration: RegistrationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role([Role.ATTENDEE, Role.ORGANIZER, Role.ADMIN]))
):
    """Register an attendee for an event. Any authenticated user can register."""
    db_registration = RegistrationService.create_registration(db, registration)
    if not db_registration:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to register attendee or event is at capacity"
        )
    return db_registration


@router.get("/{registration_id}", response_model=RegistrationSchema)
async def get_registration(
    registration_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role([Role.ATTENDEE, Role.ORGANIZER, Role.ADMIN]))
):
    """Get registration by ID."""
    registration = RegistrationService.get_registration(db, registration_id)
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )
    return registration


@router.get("/event/{event_id}", response_model=List[RegistrationSchema])
async def get_event_registrations(
    event_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role([Role.ORGANIZER, Role.ADMIN]))
):
    """Get all registrations for an event. Requires Organizer or Admin role."""
    return RegistrationService.get_registrations_by_event(db, event_id, skip=skip, limit=limit)


@router.get("/email/{email}", response_model=List[RegistrationSchema])
async def get_registrations_by_email(
    email: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role([Role.ORGANIZER, Role.ADMIN]))
):
    """Get registrations by attendee email. Requires Organizer or Admin role."""
    registrations = RegistrationService.get_registrations_by_email(db, email)
    if not registrations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No registrations found for this email"
        )
    return registrations


@router.put("/{registration_id}", response_model=RegistrationSchema)
async def update_registration(
    registration_id: int,
    registration: RegistrationUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role([Role.ORGANIZER, Role.ADMIN]))
):
    """Update registration details. Requires Organizer or Admin role."""
    db_registration = RegistrationService.update_registration(db, registration_id, registration)
    if not db_registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )
    return db_registration


@router.post("/{registration_id}/check-in", response_model=RegistrationSchema)
async def check_in_registration(
    registration_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role([Role.ATTENDEE, Role.ORGANIZER, Role.ADMIN]))
):
    """Check in a registration for the event."""
    db_registration = RegistrationService.check_in_registration(db, registration_id)
    if not db_registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )
    return db_registration


@router.delete("/{registration_id}/cancel", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_registration(
    registration_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role([Role.ATTENDEE, Role.ORGANIZER, Role.ADMIN]))
):
    """Cancel a registration."""
    success = RegistrationService.cancel_registration(db, registration_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )
    return None


@router.get("/event/{event_id}/stats")
async def get_registration_stats(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role([Role.ORGANIZER, Role.ADMIN]))
):
    """Get registration statistics for an event. Requires Organizer or Admin role."""
    stats = RegistrationService.get_event_registrations_stats(db, event_id)
    return stats
