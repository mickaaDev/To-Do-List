from ..db.database import Session, engine


def get_db():
    with Session(engine) as session:
        yield session
