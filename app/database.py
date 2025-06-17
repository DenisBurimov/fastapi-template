from sqlmodel import create_engine, Session
from config import Settings


CFG = Settings()

connect_args = {"check_same_thread": False}

if CFG.APP_ENV == "testing":
    engine = create_engine(CFG.TESTING_DATABASE_URL, connect_args=connect_args)
else:
    engine = create_engine(CFG.DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session
