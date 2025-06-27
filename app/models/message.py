from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Column, String, Text, Relationship
from uuid import uuid4


def gen_uuid():
    return str(uuid4)


if TYPE_CHECKING:
    from .user import User


class Message(SQLModel, table=True):
    __tablename__ = "messages"

    uid: Optional[str] = Field(default_factory=gen_uuid, sa_column=Column(String(36), unique=True, primary_key=True))
    content: str = Field(sa_column=Column(Text, nullable=True))
    user_id: str = Field(foreign_key="users.uid")

    user: Optional[User] = Relationship(back_populates="messages")
