from app.models import UserLoginData


def login(client, username, password, auth_testing=False):
    response = client.post(
        "/api/auth/login",
        json=UserLoginData(
            username=username,
            password=password,
        ).model_dump(),
    )
    if auth_testing:
        return response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["access_token"]
    token = response_data["access_token"]
    return token
