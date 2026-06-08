import asyncio
from dotenv import load_dotenv
load_dotenv()

import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.feedback_model import Feedback
from app.models.speaker_profile_model import SpeakerProfile

async def test_mongo():
    try:
        MONGODB_URI = os.getenv("MONGODB_URI")
        client = AsyncIOMotorClient(MONGODB_URI)
        mongo_db = client[os.getenv("MONGO_DB_NAME", "eventpulse")]
        
        await init_beanie(
            database=mongo_db,
            document_models=[Feedback, SpeakerProfile]
        )
        print("Mongo and Beanie connected successfully")
    except Exception as e:
        import traceback
        traceback.print_exc()

asyncio.run(test_mongo())
