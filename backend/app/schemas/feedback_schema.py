"""Feedback schema for request/response validation.

Used by: app/routers/feedback.py
Model:   app/models/feedback_model.py (Beanie / MongoDB)
"""

from pydantic import BaseModel, Field
from typing import Optional


class FeedbackCreate(BaseModel):
    """Schema for creating feedback."""
    event_id: Optional[int] = None
    session_id: Optional[int] = None
    registration_id: Optional[int] = None
    rating: int = Field(..., ge=1, le=5, description="Rating between 1 and 5")
    comment: Optional[str] = None


class FeedbackUpdate(BaseModel):
    """Schema for partially updating feedback."""
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None


class FeedbackSchema(BaseModel):
    """Full feedback response schema."""
    id: Optional[str] = None
    event_id: Optional[int] = None
    session_id: Optional[int] = None
    registration_id: Optional[int] = None
    rating: int
    comment: Optional[str] = None

    class Config:
        from_attributes = True
