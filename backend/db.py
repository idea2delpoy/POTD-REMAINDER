# backend/db.py
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

DATABASE_URL = "sqlite:///./potd.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # needed for SQLite + threads
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    last_seen = Column(DateTime, default=datetime.utcnow)

    schedules = relationship("Schedule", back_populates="user", cascade="all, delete-orphan")


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    platform = Column(String)
    time = Column(String)  # "HH:MM"
    repeat = Column(String)  # "daily" / "once"
    enabled = Column(Boolean, default=True)
    last_executed = Column(String, nullable=True)  # "YYYY-MM-DD"

    user = relationship("User", back_populates="schedules")


def init_db():
    Base.metadata.create_all(bind=engine)
