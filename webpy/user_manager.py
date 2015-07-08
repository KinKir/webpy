from webpy import app
from webpy.database import db_session
from webpy.models import User
from sqlalchemy.sql import exists


def add_user(name, email):
    if not user_exists(name, email):
        new_user = User(name, email)
        print("Creating User:", new_user)
        db_session.add(new_user)
        db_session.commit()


def user_exists(name, email):
    stmt = exists().where(User.username == name and User.email == email)
    return db_session.query(stmt).one()[0]
