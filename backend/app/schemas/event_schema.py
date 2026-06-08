"""Event schema for request/response validation."""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List


class EventBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    location: Optional[str] = None
    start_date: datetime
    end_date: datetime
    max_attendees: Optional[int] = None
    organizer: Optional[str] = None


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    max_attendees: Optional[int] = None
    status: Optional[str] = None


class EventSchema(EventBase):
    id: int
    status: str
    current_attendees: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True
