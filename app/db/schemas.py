from pydantic import BaseModel
from datetime import datetime
from sqlmodel import SQLModel, Field


class TaskBase(SQLModel):
    id: int


class Task(TaskBase):
    title: str
    description: str
    created: datetime
    owner_id: int

    class Config:
        orm_mode = True


class TaskCreate(SQLModel):
    owner_id: int
    title: str
    description: str
    completed: bool | None = False


class UserBase(SQLModel):
    pass


class UserCreate(UserBase):
    username: str
    password: str


class User(UserBase):
    id: int
    username: str
    full_name: str | None = None
    disabled: bool | None = None
    tasks: list[Task] = []

    class Config:
        orm_mode = True


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None
