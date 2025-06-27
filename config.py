import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    APP_ENV: str = "development"
    APP_NAME: str = "FastAPI"
    APP_FOLDER: str = str(Path(__file__).resolve().parent)
    SECRET_KEY: str = "very_strong_secret_key"
    DATABASE_URL: str = "sqlite:///db.sqlite3"
    TESTING_DATABASE_URL: str = "sqlite:///:memory:"

    LDAP_SERVER: str = "ldap://ldap-ldap.us-west-2.amazonaws.com"
    LDAP_USER_FORMAT: str = ""
    LDAP_BASE_DN: str = ""
    LDAP_SEARCH_FILTER: str = ""

    JWT_SECRET_KEY: str = "some_very_special_and_complicated_secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30

    ADMIN_USERNAME: str = os.environ.get("ADMIN_USERNAME", "")
    ADMIN_PASSWORD: str = os.environ.get("ADMIN_PASSWORD", "")
    ADMIN_EMAIL: str = os.environ.get("ADMIN_EMAIL", "")

    SAP_URL: str = os.environ.get("SAP_URL", "")
    OPENAI_API_KEY: str = ""

    model_config = SettingsConfigDict(extra="allow", env_file=(".env"))
