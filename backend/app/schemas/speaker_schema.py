"""Speaker schema for request/response validation."""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class SpeakerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    bio: Optional[str] = None
    company: Optional[str] = None
    expertise: Optional[str] = None
    profile_url: Optional[str] = None


class SpeakerCreate(SpeakerBase):
    pass


class SpeakerUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    company: Optional[str] = None
    expertise: Optional[str] = None
    profile_url: Optional[str] = None


class SpeakerSchema(SpeakerBase):
    """Full speaker detail schema (used for GET /speakers/{id})."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SpeakerListResponse(SpeakerBase):
    """Speaker list schema — includes sessions_count per speaker (used for GET /speakers/)."""
    id: int
    sessions_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
