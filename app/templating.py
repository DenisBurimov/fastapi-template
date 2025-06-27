import os
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader, pass_context
from starlette.middleware.errors import TEMPLATE

from sqlmodel import Session, select
from app.database import engine
from app import models as m
from config import Settings


CFG = Settings()

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")

templates = Jinja2Templates(directory=TEMPLATE_DIR)


@pass_context
def get_current_user(ctx):
    request = ctx.get("request")
    user_id = request.session.get("user_id")

    if not user_id:
        return None

    session = Session(engine)
    current_user = session.scalar(select(m.User).where(m.User.uid == user_id))
    return m.UserProfile(
        name=current_user.name,
        email=current_user.email,
        role=current_user.role,
    )


templates.env.globals["current_user"] = get_current_user
templates.env.globals["APP_NAME"] = CFG.APP_NAME
