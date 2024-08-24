from typing import Optional
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
    completed: Optional[bool] = False



class UserBase(SQLModel):
    pass


class UserCreate(UserBase):
    username: str
    password: str


class User(UserBase):
    id: int
    username: str
    full_name: Optional[str] = None 
    disabled: Optional[str] = None 
    tasks: list[Task] = []

    class Config:
        orm_mode = True


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: Optional[str] = None 
