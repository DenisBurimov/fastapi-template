import os
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
from starlette.middleware.errors import TEMPLATE

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")

templates = Jinja2Templates(directory=TEMPLATE_DIR)

templates.env.globals["APP_NAME"] = "JARVIS"
