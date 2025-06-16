from sqlmodel import create_engine, Session
from config import Settings


CFG = Settings()

connect_args = {"check_same_thread": False}

if CFG.APP_ENV == "testing":
    database_url = CFG.TESTING_DATABASE_URL
else:
    database_url = CFG.DATABASE_URL

engine = create_engine(database_url, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session
