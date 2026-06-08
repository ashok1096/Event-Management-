"""PostgreSQL database connection and configuration."""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Environment variables are loaded in main.py (load_dotenv called there)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/eventpulse"
)

# Ensure sync driver in URL
if DATABASE_URL.startswith("postgresql+asyncpg"):
    DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

Base = declarative_base()

def get_db():
    """Generator for DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
