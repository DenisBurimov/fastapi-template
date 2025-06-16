import requests
from invoke import task
from app.models import UserLoginData
from config import Settings


CFG = Settings()


@task
def parse_files(c):
    login_response = requests.post(
        "http://127.0.0.1:8000/api/auth/login",
        json=UserLoginData(
            username=CFG.ADMIN_USERNAME,
            password=CFG.ADMIN_PASSWORD,
        ).model_dump(),
    )
    response_data = login_response.json()
    # print(response_data)
    token = response_data["access_token"]
    headers = {"Authorization": "Bearer " + token}
    response = requests.get("http://127.0.0.1:8000/api/checks/parse", headers=headers)
    print(response.text)
