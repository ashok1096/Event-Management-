"""repositories package — exports all repository classes."""

from app.repositories.base_repository import BaseRepository
from app.repositories.event_repository import EventRepository
from app.repositories.speaker_repository import SpeakerRepository
from app.repositories.registration_repository import RegistrationRepository

__all__ = [
    "BaseRepository",
    "EventRepository",
    "SpeakerRepository",
    "RegistrationRepository",
]
