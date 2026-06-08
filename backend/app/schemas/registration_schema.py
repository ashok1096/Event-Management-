"""Registration schema for request/response validation."""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class RegistrationBase(BaseModel):
    event_id: int
    attendee_name: str = Field(..., min_length=1, max_length=255)
    attendee_email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    designation: Optional[str] = None


class RegistrationCreate(RegistrationBase):
    pass


class RegistrationUpdate(BaseModel):
    attendee_name: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    designation: Optional[str] = None


class RegistrationSchema(RegistrationBase):
    id: int
    registration_code: str
    status: str
    is_checked_in: bool
    checked_in_at: Optional[datetime] = None
    payment_status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
