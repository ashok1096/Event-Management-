"""MongoDB Feedback document (Beanie ODM)."""

from beanie import Document
from typing import Optional
from datetime import datetime, timezone

class Feedback(Document):
    event_id: Optional[int] = None
    session_id: Optional[int] = None
    registration_id: Optional[int] = None
    rating: int  # 1-5 rating
    comment: Optional[str] = None
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)

    class Settings:
        name = "feedbacks"