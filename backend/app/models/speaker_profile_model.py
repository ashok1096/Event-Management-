"""MongoDB SpeakerProfile document (Beanie ODM).

Stores extended speaker profiles — bio, past talks, social links —
separately from the PostgreSQL Speaker record.
"""

from beanie import Document
from typing import List, Optional
from pydantic import Field


class SpeakerProfile(Document):
    speaker_id: int  # FK to PostgreSQL speakers.id
    bio: Optional[str] = None
    company: Optional[str] = None
    expertise: Optional[str] = None
    past_talks: List[str] = Field(default_factory=list)
    social_links: dict = Field(default_factory=dict)
    # e.g. {"linkedin": "...", "twitter": "...", "github": "..."}
    photo_url: Optional[str] = None

    class Settings:
        name = "speaker_profiles"
