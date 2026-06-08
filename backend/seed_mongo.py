import asyncio
import os

# Add backend directory to sys.path
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.speaker_profile_model import SpeakerProfile
from app.models.feedback_model import Feedback

async def seed_mongo():
    try:
        MONGODB_URI = os.getenv("MONGODB_URI")
        client = AsyncIOMotorClient(MONGODB_URI)
        mongo_db = client[os.getenv("MONGO_DB_NAME", "eventpulse")]
        
        await init_beanie(
            database=mongo_db,
            document_models=[Feedback, SpeakerProfile]
        )
        print("Connected to MongoDB")
        
        # Insert a dummy speaker profile to force DB creation
        dummy = SpeakerProfile(
            speaker_id=9999,
            bio="Dummy bio to initialize database",
            company="Dummy Company"
        )
        await dummy.insert()
        print("Inserted dummy speaker profile. Database 'eventpulse' is now permanently created.")
    except Exception as e:
        import traceback
        traceback.print_exc()

asyncio.run(seed_mongo())
