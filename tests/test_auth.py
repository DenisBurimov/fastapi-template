from fastapi.testclient import TestClient
from .utils import login


def test_login(client: TestClient, session):
    response = login(client, "admin", "admin", auth_testing=True)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["token_type"] == "Bearer"
    assert response_data["access_token"]


def test_login_failed(client: TestClient, session):
    response = login(client, "admin", "wrong_password", auth_testing=True)
    assert response.status_code == 403
    response_data = response.json()
    assert response_data["detail"] == "Password mismatch"


def test_get_access(client: TestClient, session):
    token = login(client, "admin", "admin")

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/auth/profile", headers=headers)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == "admin"


def test_ui_auth(client: TestClient, session):
    response = client.post(
        "/auth/login",
        data={
            "username": "admin",
            "password": "admin",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200


def test_ui_logout(client: TestClient):
    response = client.get("/auth/logout")
    assert response.status_code == 200
