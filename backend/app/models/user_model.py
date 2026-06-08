from sqlalchemy import Column, Integer, String, Enum
from app.database.postgres import Base
from app.models.role_enum import Role


class User(Base):
    __tablename__ = "users"

    user_id = Column("id", Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column("hashed_password", String(255), nullable=False)
    role = Column(Enum(Role), nullable=False, default=Role.ATTENDEE)