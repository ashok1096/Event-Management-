"""FastAPI main application entry point."""

import os
import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# ── Load env vars ONCE here before any other import reads os.getenv ──────────
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.utils.logging_config import setup_logging
from app.utils.cache import init_cache, close_cache
from app.database.mongo import init_mongo
from app.database.postgres import engine, Base
from app.middleware.error_handler import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)
from app.routers import events, registrations, sessions, checkins, speakers, feedback, auth
import app.models

# ── Structured JSON logging ───────────────────────────────────────────────────
setup_logging(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

# ── SlowAPI rate limiter (default: 60 requests/minute per IP) ─────────────────
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[os.getenv("RATE_LIMIT", "60/minute")],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("EventPulse starting up…")

    logger.info("Creating PostgreSQL tables…")
    Base.metadata.create_all(bind=engine)

    # ── Seed hardcoded admin account ──────────────────────────────────────────
    from app.database.postgres import SessionLocal
    from app.models.user_model import User
    from app.models.role_enum import Role
    from app.auth.security import hash_password

    db = SessionLocal()
    try:
        admin_email = "admin@gmail.com"
        existing_admin = db.query(User).filter(User.email == admin_email).first()
        if not existing_admin:
            admin_user = User(
                name="Admin",
                email=admin_email,
                password=hash_password("admin"),
                role=Role.ADMIN,
            )
            db.add(admin_user)
            db.commit()
            logger.info("✅ Default admin account seeded (admin@gmail.com)")
        else:
            logger.info("ℹ️  Admin account already exists, skipping seed.")
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Failed to seed admin account: {e}")
    finally:
        db.close()

    logger.info("Connecting to MongoDB…")
    await init_mongo()

    logger.info("Initialising Redis cache…")
    await init_cache()

    logger.info("All services ready.")
    yield

    logger.info("EventPulse shutting down…")
    await close_cache()


# ── FastAPI app ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="EventPulse API",
    description="Conference and Multi-Session Event Management Portal",
    version="1.0.0",
    lifespan=lifespan,
)

# ── Rate limiting middleware ──────────────────────────────────────────────────
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# ── CORS (restricted to known frontend origins) ───────────────────────────────
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173,http://localhost:5174"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Global error handlers ─────────────────────────────────────────────────────
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# ── OAuth2 bearer scheme (registers BearerAuth in Swagger UI automatically) ──
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(events.router)
app.include_router(registrations.router)
app.include_router(sessions.router)
app.include_router(checkins.router)
app.include_router(speakers.router)
app.include_router(feedback.router)


# ── Health / meta endpoints ───────────────────────────────────────────────────
@app.get("/")
async def root():
    return {
        "message": "EventPulse API - Conference Management Platform",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Server is running"}


@app.get("/api/v1/docs")
async def docs():
    return {
        "message": "API Documentation",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )