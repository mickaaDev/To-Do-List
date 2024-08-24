import os

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlmodel import create_engine, SQLModel, Session

load_dotenv()

# Example of DATABASE_URI
#DATABASE_URI=postgresql://<DB_USER>:<DB_PASSWORD>@<DB_HOST>:<DB_PORT>/<DB_NAME>
engine = create_engine(
    os.getenv("DATABASE_URI")
)

Base = declarative_base()

def init_db():
    SQLModel.metadata.create_all(engine)
