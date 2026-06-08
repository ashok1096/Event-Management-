import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.models.feedback_model import Feedback
from app.models.speaker_profile_model import SpeakerProfile

# Environment variables are loaded once in main.py; no need to call load_dotenv here.
MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    raise RuntimeError("MONGODB_URI missing in .env file")

client = AsyncIOMotorClient(MONGODB_URI)
mongo_db = client[os.getenv("MONGO_DB_NAME", "eventpulse")]


async def init_mongo():
    await init_beanie(
        database=mongo_db,
        document_models=[Feedback, SpeakerProfile]   # ← SpeakerProfile registered here
    )