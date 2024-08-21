import os

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlmodel import create_engine, SQLModel, Session

load_dotenv()

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://postgres:{os.getenv('postgressql_password')}"
    f"@{os.getenv('postgressql_server')}/todolist"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    SQLModel.metadata.create_all(engine)
