from fastapi.testclient import TestClient


def test_root(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    response_data = response.json()
    routes = response_data.get("routes")
    assert routes
