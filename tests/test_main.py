def test_root(client):
    response = client.get("/health")
    assert response.status_code == 200
    response_data = response.json()
    routes = response_data.get("routes")
    assert routes
