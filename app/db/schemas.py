from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class TaskBase(BaseModel):
    id: int
    title: str
    description: Optional[str] = None

class Task(TaskBase):
    created: datetime
    completed: bool = False
    owner_id: int

    class Config:
        orm_mode = True 

class TaskCreate(TaskBase):
    owner_id: int

class UserBase(BaseModel):
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

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None