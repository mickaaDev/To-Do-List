import logging
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta

from ..db import models
from ..db import crud

from ..utils.dependencies import get_db
from ..db import schemas
from ..db.database import engine, init_db
from ..db.schemas import Token, User
from .auth import (
    authenticate_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_active_user
)



logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    filemode="a",
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/users/", response_model=schemas.User)
def sign_up(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")

    logger.info(f"User is signed up '{user.username}'.")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/user/{user_id}", response_model=schemas.User)
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
        logger.info(f"User '{db_user.username}' was deleted from DB.")
        return {"detail": "User deleted successfully!"}
    return HTTPException(
        status_code=400,
        detail="User does not exist in DB.",
        headers={"X-Error": "There goes my error"}
    ) 


@app.patch("/task/{task_id}/", response_model=schemas.Task)
def update_task(
    task_id: int,
    task_update: schemas.TaskCreate,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not crud.task_belongs_user(db=db, task_id=task_id, user=user):
        raise HTTPException(
            status_code=404,
            detail="This task does not belongs to the current user"
        )
    task = crud.update_task(db, task_id=task_id, task_update=task_update)
    logger.info(f"User '{user.username}' updated the task '{task.title}'.")
    if task is None:
        raise HTTPException(status_code=404, detail="Unsuccessful update.")

    return task


@app.post("/users/task/", response_model=schemas.Task)
def create_task_for_user(
    task: schemas.TaskCreate,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.info(f"User '{user.username}' created the task '{task.title}'.")
    return crud.create_task(db=db, task=task, user_id=user.id)


@app.get("/tasks/", response_model=list[schemas.Task])
async def read_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks


@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user)
):

    db_task = crud.get_task(db, task_id=task_id)
    if db_task:
        crud.remove_task(db, task_id=task_id)
        logger.info(f"Task with title '{db_task.title}' was deleted.")
        return {"detail": "Task was deleted"}
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
        logger.info(f"Some user could not sign in. Error message: Incorrect username or password . Status code 400.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    logger.info(f"User '{user.username}', received access token to sign in.")
    return Token(access_token=access_token, token_type='bearer')


@app.get("/user/me/")
async def read_user_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user
