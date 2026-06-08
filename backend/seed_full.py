import asyncio
import os
import sys
from datetime import datetime, timedelta, timezone
import random

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.database.postgres import SessionLocal
from app.models.event_model import Event
from app.models.speaker_model import Speaker
from app.models.session_model import Session as SessionModel
from app.models.registration_model import Registration
from app.models.checkin_model import CheckIn
from app.models.feedback_model import Feedback
from app.models.speaker_profile_model import SpeakerProfile
from app.models.user_model import User

async def seed_mongo():
    MONGODB_URI = os.getenv("MONGODB_URI")
    client = AsyncIOMotorClient(MONGODB_URI)
    mongo_db = client[os.getenv("MONGO_DB_NAME", "eventpulse")]
    await init_beanie(database=mongo_db, document_models=[Feedback, SpeakerProfile])

    # Clear existing feedback
    await Feedback.find_all().delete()
    print("Cleared existing MongoDB Feedback.")
    return True

def seed_postgres():
    from sqlalchemy import text
    db = SessionLocal()
    
    # Clear existing data and reset IDs to 1
    db.execute(text("TRUNCATE TABLE checkins, registrations, sessions, speakers, events RESTART IDENTITY CASCADE"))
    db.commit()
    print("Cleared existing PostgreSQL data and reset IDs to 1.")

    now = datetime.now(timezone.utc)

    # 1. Create Events
    events = [
        Event(
            title="Tech Innovators Summit 2026",
            description="The premier conference for emerging technologies and startup innovation.",
            location="Chennai Trade Centre, Chennai",
            start_date=now + timedelta(days=10),
            end_date=now + timedelta(days=12),
            max_attendees=500,
            status="upcoming",
            organizer="TechCrunch"
        ),
        Event(
            title="Global AI Conference",
            description="Deep dive into Artificial Intelligence, LLMs, and future prospects.",
            location="Codissia Trade Fair Complex, Coimbatore",
            start_date=now - timedelta(days=5),
            end_date=now - timedelta(days=3),
            max_attendees=1000,
            status="completed",
            organizer="AI World"
        ),
        Event(
            title="Cloud Native Expo",
            description="Everything about Kubernetes, Docker, and Cloud Native Architectures.",
            location="BIEC, Bangalore",
            start_date=now + timedelta(days=30),
            end_date=now + timedelta(days=31),
            max_attendees=300,
            status="upcoming",
            organizer="CNCF"
        )
    ]
    db.add_all(events)
    db.commit()
    
    # Refresh to get IDs
    for e in events: db.refresh(e)

    # 2. Create Speakers
    speakers = [
        Speaker(name="Dr. Alice Chen", email="alice@ai-world.org", bio="Leading researcher in LLMs.", company="OpenAI", expertise="Artificial Intelligence"),
        Speaker(name="Bob Smith", email="bob@techcrunch.com", bio="Investor and tech enthusiast.", company="Sequoia", expertise="Venture Capital"),
        Speaker(name="Carol Williams", email="carol@cncf.io", bio="Kubernetes core contributor.", company="Google Cloud", expertise="Cloud Native"),
        Speaker(name="David Jones", email="david@innovate.tech", bio="Serial entrepreneur.", company="Innovate Tech", expertise="Startups")
    ]
    db.add_all(speakers)
    db.commit()
    for s in speakers: db.refresh(s)

    # 3. Create Sessions
    sessions = []
    # Tech Innovators Summit
    sessions.append(SessionModel(event_id=events[0].id, speaker_id=speakers[1].id, title="Future of Funding", start_time=events[0].start_date + timedelta(hours=10), end_time=events[0].start_date + timedelta(hours=11), location="Room A", capacity=200, session_code="TIS-101"))
    sessions.append(SessionModel(event_id=events[0].id, speaker_id=speakers[3].id, title="Building from Scratch", start_time=events[0].start_date + timedelta(hours=13), end_time=events[0].start_date + timedelta(hours=14), location="Room B", capacity=150, session_code="TIS-102"))
    # Global AI Conference
    sessions.append(SessionModel(event_id=events[1].id, speaker_id=speakers[0].id, title="LLMs in 2026", start_time=events[1].start_date + timedelta(hours=9), end_time=events[1].start_date + timedelta(hours=10, minutes=30), location="Main Hall", capacity=800, session_code="GAI-001"))
    # Cloud Native Expo
    sessions.append(SessionModel(event_id=events[2].id, speaker_id=speakers[2].id, title="Kubernetes 2.0", start_time=events[2].start_date + timedelta(hours=10), end_time=events[2].start_date + timedelta(hours=12), location="Hall 1", capacity=300, session_code="CNE-001"))
    
    db.add_all(sessions)
    db.commit()
    for s in sessions: db.refresh(s)

    # 4. Create Registrations
    attendee_names = [
        "Kirthiga", "Ashok", "Navanith", "Bhavya Singh", "Chaitanya Patel", 
        "Deepa Reddy", "Eshaan Iyer", "Gauri Menon", "Hari Krishnan", "Isha Desai", 
        "Jayant Verma", "Karthik Raj", "Lakshmi Narayan", "Manoj Tiwari", "Nandini Gupta", 
        "Omkar Joshi", "Priya Venkatesh", "Rahul Nair", "Sneha Pillai", "Tarun Malhotra"
    ]
    
    registrations = []
    for i in range(0, 10):
        name = attendee_names[i]
        email = f"{name.lower().replace(' ', '')}@gmail.com"
        reg = Registration(
            event_id=events[0].id,
            attendee_name=name,
            attendee_email=email,
            company="Tech Corp",
            designation="Developer",
            registration_code=f"REG-TIS-{i+1}",
            status="registered",
            is_checked_in=(i % 3 == 0)
        )
        if reg.is_checked_in:
            reg.checked_in_at = events[0].start_date
            events[0].current_attendees += 1
        registrations.append(reg)
    
    for i in range(10, 20):
        name = attendee_names[i]
        email = f"{name.lower().replace(' ', '')}@gmail.com"
        reg = Registration(
            event_id=events[1].id,
            attendee_name=name,
            attendee_email=email,
            company="AI Inc",
            designation="Data Scientist",
            registration_code=f"REG-GAI-{i+1}",
            status="registered",
            is_checked_in=True
        )
        reg.checked_in_at = events[1].start_date
        events[1].current_attendees += 1
        registrations.append(reg)

    db.add_all(registrations)
    db.commit()
    for r in registrations: db.refresh(r)

    # 5. Create CheckIns for checked-in registrations
    checkins = []
    for r in registrations:
        if r.is_checked_in:
            checkins.append(CheckIn(
                registration_id=r.id,
                checkin_type="registration",
                timestamp=r.checked_in_at,
                location="Main Entrance"
            ))
            # Session check-in
            session_id = sessions[0].id if r.event_id == events[0].id else sessions[2].id
            checkins.append(CheckIn(
                registration_id=r.id,
                session_id=session_id,
                checkin_type="session",
                timestamp=r.checked_in_at + timedelta(minutes=15),
                location="Session Room"
            ))
    
    db.add_all(checkins)
    db.commit()

    print("PostgreSQL seeded successfully.")
    db.close()
    return events, sessions

async def seed_feedback(events, sessions):
    feedbacks = [
        Feedback(
            event_id=events[1].id,
            session_id=sessions[2].id,
            registration_id=11, # roughly corresponding to our data
            rating=5,
            comment="Amazing insights on LLMs! Truly transformative.",
            created_at=events[1].start_date + timedelta(days=1)
        ),
        Feedback(
            event_id=events[1].id,
            session_id=sessions[2].id,
            registration_id=12,
            rating=4,
            comment="Great session, but a bit too fast paced.",
            created_at=events[1].start_date + timedelta(days=1, hours=2)
        ),
        Feedback(
            event_id=events[0].id,
            registration_id=1,
            rating=5,
            comment="Looking forward to this event!",
            created_at=datetime.now(timezone.utc)
        )
    ]
    await Feedback.insert_many(feedbacks)
    print("MongoDB Feedback seeded successfully.")

async def main():
    await seed_mongo()
    events, sessions = seed_postgres()
    await seed_feedback(events, sessions)
    print("Database seeding complete!")

if __name__ == "__main__":
    asyncio.run(main())
