import pytest
from sqlmodel import SQLModel, Session, create_engine
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from app import models as m, create_app


@pytest.fixture(scope="session")
def mock_engine():
    return create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )


@pytest.fixture(scope="function")
def session(mock_engine):
    SQLModel.metadata.create_all(bind=mock_engine)
    with Session(mock_engine) as session:
        yield session
    SQLModel.metadata.drop_all(bind=mock_engine)


@pytest.fixture(scope="function")
def client(session):
    def override_get_session():
        yield session

    app = create_app(override_get_session)

    # Prepopulate a test user
    user = m.User(
        name="admin",
        # password="admin",
        email="admin@mail.com",
        role=m.UserRole.admin.value,
    )
    user.password = "admin"
    session.add(user)
    session.commit()

    yield TestClient(app)
