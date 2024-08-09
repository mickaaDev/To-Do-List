from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class User(Base):
    __tablename__ = "users"

    username = Column(String, unique=True, index=True)
    id = Column(Integer, primary_key=True, autoincrement=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)

    tasks = relationship("Task", back_populates="owner")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created = Column(DateTime, default=datetime.utcnow)
    completed = Column(Boolean, default=False)

    owner = relationship("User", back_populates="tasks")
