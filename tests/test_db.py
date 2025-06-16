from fastapi.testclient import TestClient
from sqlmodel import select
from app import models as m


def test_db(client: TestClient, session):
    users = session.scalars(select(m.User)).all()
    assert users
