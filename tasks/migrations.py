from invoke import task
from config import Settings
from alembic.config import Config
from alembic import command
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s")


CFG = Settings()


@task(help={"message": "revision message"})
def db_migrate(c, message="auto_revision"):
    c.run(f'alembic revision --autogenerate -m "{message}"')


@task
def db_upgrade(c):
    logger.info("DATABASE_URL: %s", CFG.DATABASE_URL)
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", CFG.DATABASE_URL)
    # c.run("alembic upgrade head")
    try:
        command.upgrade(alembic_cfg, "head")
        logger.info("alembic upgrade head run successfully")
    except Exception as e:
        logger.error("alembic upgrade head failed: %s", e)
