import sys
from pathlib import Path
from invoke import task
from sqlmodel import Session, select
from IPython import embed


PROJECT_ROOT = Path(__file__).parent.parent
print(PROJECT_ROOT)
sys.path.insert(0, str(PROJECT_ROOT))


@task
def shell(c):
    from app import create_app, models as m
    from app.database import engine

    app = create_app()
    session = Session(engine)

    context = {
        "app": app,
        "session": session,
        "m": m,
        "s": select,
    }
    # embed(user_ns=context, colors="Linux")
    embed(user_ns=context, colors="LightBG")
