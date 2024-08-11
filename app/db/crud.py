from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from . import models
from . import schemas
from ..api.auth import get_password_hashed


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(
        models.User.username == username
    ).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()


def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def remove_task(db: Session, task_id: int):
    db_task = get_task(db, task_id=task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
        return {"detail": "User deleted successfully"}
    else:
        return HTTPException(status_code=404, detail="Task not found")


def create_user(db: Session, user: schemas.UserCreate):
    if user.username == "":
        raise HTTPException(status_code=404, detail="username cannot be empty")
    if user.password == "":
        raise HTTPException(status_code=404, detail="Password cannot be empty")
    hashed_password = get_password_hashed(user.password)
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        owner_id=user_id,
        created=datetime.utcnow(),
        completed=False
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(
        db: Session,
        task_id: schemas.Task,
        task_update: schemas.Task
):
    task = get_task(db, task_id=task_id)
    if not task:
        return HTTPException(status_code=400, detail="Task does not exists")
    if task_update.title:
        task.title = task_update.title
    if task_update.description:
        task.description = task_update.description
    if task_update.completed is not None:
        task.completed = task_update.completed
    db.commit()
    return task


def task_belongs_user(
    db: Session,
    task_id: int,
    user: schemas.User
):

    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        return False
    return task.owner_id == user.id


def remove_user(db: Session, user_id: int):
    db_user = get_user(db, user_id=user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return {"detail": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")
