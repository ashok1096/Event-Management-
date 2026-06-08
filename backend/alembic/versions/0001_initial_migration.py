"""Initial migration — creates all EventPulse tables.

Revision ID: 0001
Revises: 
Create Date: 2026-06-07
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── users ──────────────────────────────────────────────────────────────────
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False, unique=True, index=True),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("role", sa.String(50), nullable=False, default="attendee"),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── events ─────────────────────────────────────────────────────────────────
    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("title", sa.String(255), nullable=False, index=True),
        sa.Column("description", sa.Text()),
        sa.Column("location", sa.String(255)),
        sa.Column("start_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("max_attendees", sa.Integer()),
        sa.Column("current_attendees", sa.Integer(), default=0),
        sa.Column("status", sa.String(50), default="upcoming"),
        sa.Column("organizer", sa.String(255)),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── speakers ───────────────────────────────────────────────────────────────
    op.create_table(
        "speakers",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(255), nullable=False, index=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True, index=True),
        sa.Column("bio", sa.Text()),
        sa.Column("company", sa.String(255)),
        sa.Column("expertise", sa.String(255)),
        sa.Column("profile_url", sa.String(255)),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── sessions ───────────────────────────────────────────────────────────────
    op.create_table(
        "sessions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("event_id", sa.Integer(), sa.ForeignKey("events.id"), nullable=False, index=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("speaker_id", sa.Integer(), sa.ForeignKey("speakers.id"), index=True),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("location", sa.String(255)),
        sa.Column("capacity", sa.Integer()),
        sa.Column("current_attendees", sa.Integer(), default=0),
        sa.Column("session_code", sa.String(20), unique=True, index=True),
        sa.Column("status", sa.String(50), default="scheduled"),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("idx_session_event_id", "sessions", ["event_id"])
    op.create_index("idx_session_speaker_id", "sessions", ["speaker_id"])
    op.create_index("idx_session_status", "sessions", ["status"])
    op.create_index("idx_session_start_time", "sessions", ["start_time"])

    # ── registrations ──────────────────────────────────────────────────────────
    op.create_table(
        "registrations",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("event_id", sa.Integer(), sa.ForeignKey("events.id"), nullable=False, index=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True, index=True),
        sa.Column("attendee_name", sa.String(255), nullable=False),
        sa.Column("attendee_email", sa.String(255), nullable=False, index=True),
        sa.Column("phone", sa.String(20)),
        sa.Column("company", sa.String(255)),
        sa.Column("designation", sa.String(255)),
        sa.Column("registration_code", sa.String(20), unique=True, index=True),
        sa.Column("status", sa.String(50), default="registered"),
        sa.Column("is_checked_in", sa.Boolean(), default=False),
        sa.Column("checked_in_at", sa.DateTime(timezone=True)),
        sa.Column("payment_status", sa.String(50), default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("user_id", "event_id", name="uq_user_event_registration"),
        sa.UniqueConstraint("event_id", "attendee_email", name="uq_event_email_registration"),
    )
    op.create_index("idx_attendee_email", "registrations", ["attendee_email"])
    op.create_index("idx_registration_status", "registrations", ["status"])

    # ── checkins ───────────────────────────────────────────────────────────────
    op.create_table(
        "checkins",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("registration_id", sa.Integer(), sa.ForeignKey("registrations.id"), nullable=False, index=True),
        sa.Column("session_id", sa.Integer(), sa.ForeignKey("sessions.id"), index=True),
        sa.Column("checkin_type", sa.String(50), default="session"),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("location", sa.String(255)),
        sa.Column("device_id", sa.String(100)),
        sa.UniqueConstraint("registration_id", "session_id", name="uix_registration_session_checkin"),
    )
    op.create_index("idx_checkin_registration_id", "checkins", ["registration_id"])
    op.create_index("idx_checkin_session_id", "checkins", ["session_id"])


def downgrade() -> None:
    op.drop_table("checkins")
    op.drop_table("registrations")
    op.drop_table("sessions")
    op.drop_table("speakers")
    op.drop_table("events")
    op.drop_table("users")
