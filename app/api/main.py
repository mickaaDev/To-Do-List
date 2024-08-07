from fastapi import FastAPI, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta

from ..db import models

from ..db import crud

from . import auth

from ..utils.dependencies import get_db
from ..db import schemas
from ..db.database import SessionLocal, engine
from .auth import (
    authenticate_user, 
    ACCESS_TOKEN_EXPIRE_MINUTES, 
    create_access_token,
    get_current_active_user
)
from ..db.schemas import Token, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):    
    db_user = crud.get_user(db, user_id=user_id)
    if db_user:
        crud.remove_user(db, user_id=user_id)
        return {"detail": "User deleted successfully!"}
    return HTTPException(
        status_code=400, 
        detail="User does not exist in DB.", 
        headers={"X-Error": "There goes my error"}
    )

@app.post("/users/{user_id}/items/", response_model=schemas.Task)
def create_item_for_user(
    user_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)
):    
    return crud.create_task(db=db, task=task, user_id=user_id)

@app.get("/tasks/", response_model=list[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task:
        crud.remove_task(db, task_id=task_id)
        return {"detailed":"Task was deleted"}
    return HTTPException(
        status_code=400, 
        detail="Task does not exist in DB.", 
        headers={"X-Error": "There goes my error"}
    )

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub":user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type='bearer')

@app.get("/user/me")
async def read_user_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@app.patch("/update_task/{task_id}/")
async def update_task(
    task_id: int, 
    task_update: schemas.Task, 
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    task = crud.update_task(
        task_id=task_id,
        db=db,
        user=user,
        task_update=task_update
    )
    return {"detail":"Task was updated successfully!"}

