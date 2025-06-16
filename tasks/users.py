from invoke import task
from sqlmodel import Session, select
from app import models as m
from app.database import engine
from config import Settings


CFG = Settings()


@task
def get_users(c):
    """Print all users in the database."""
    with Session(engine) as session:
        users = session.scalars(select(m.User)).all()
        if not users:
            print("No users found.")
            return
        for user in users:
            print(f"{user.name}:{user.email}:{user.role}")


@task
def create_admin(c):
    with Session(engine) as session:
        admin = m.User(
            name=CFG.ADMIN_USERNAME,
            email=CFG.ADMIN_EMAIL,
            role=m.UserRole.admin.value,
        )
        admin.password = CFG.ADMIN_PASSWORD
        session.add(admin)
        session.commit()
    print("Admin created")


@task
def delete_users(c):
    with Session(engine) as session:
        users = session.scalars(select(m.user)).all()
        if not users:
            print("No users found.")
            return False
        for user in users:
            # for c in user.cassettes:
            #     session.delete(c)
            session.delete(user)
        try:
            session.commit()
            print("Deleted all users.")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
