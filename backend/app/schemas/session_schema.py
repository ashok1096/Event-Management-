"""Session schema for request/response validation."""

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class SessionBase(BaseModel):
    event_id: int
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    speaker_id: Optional[int] = None
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    capacity: Optional[int] = None


class SessionCreate(SessionBase):
    pass


class SessionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    speaker_id: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    capacity: Optional[int] = None


class SessionSchema(SessionBase):
    id: int
    session_code: str
    current_attendees: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
