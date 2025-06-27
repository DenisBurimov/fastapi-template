import enum
from typing import Optional
from sqlmodel import SQLModel, Field, Column, String
from passlib.context import CryptContext
from uuid import uuid4


crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRole(str, enum.Enum):
    admin = "admin"
    editor = "editor"
    viewer = "viewer"


def gen_uuid():
    return str(uuid4)


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: Optional[str] = Field(default_factory=gen_uuid, sa_column=Column(String(36), unique=True, primary_key=True))
    name: str = Field(sa_column=Column(String(32), nullable=False, unique=True))
    email: str = Field(sa_column=Column(String(255), nullable=False))
    role: str = Field(default=UserRole.viewer.value, sa_column=Column(String(12), default=UserRole.viewer.value))
    password_hash: str = Field(default="", sa_column=Column(String(512), default=""))
    activated: bool = Field(default=True)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, raw_password: str):
        self.password_hash = crypt_context.hash(raw_password)

    def verify_password(self, password: str) -> bool:
        return crypt_context.verify(password, self.password_hash)

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"


class UserLoginData(SQLModel):
    username: str
    password: str


class UserToken(SQLModel):
    access_token: str
    token_type: str


class UserProfile(SQLModel):
    name: str
    email: str
    role: str
