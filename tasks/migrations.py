from invoke import task


@task(help={"message": "revision message"})
def db_migrate(c, message="auto_revision"):
    c.run(f'alembic revision --autogenerate -m "{message}"')


@task
def db_upgrade(c):
    c.run("alembic upgrade head")
