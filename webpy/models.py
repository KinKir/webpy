from sqlalchemy import Column, Integer, String, Boolean
from webpy.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey


class Plan(Base):
    __tablename__ = 'plans'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    cpu_time = Column(Integer)
    cpu_quota = Column(Integer)
    price = Column(Integer)
    tasks = relationship('Task')

    def __init__(self, name, time, quota, price):
        self.name = name
        self.cpu_time = time
        self.cpu_quota = quota
        self.price = price

    def __repr__(self):
        return '<Plan: %r:%d:%d>' % (self.name, self.cpu_time, self.cpu_quota)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True)
    email = Column(String(120), unique=True)
    tasks = relationship('Task')

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return "<User: %r:%r>" % (self.username, self.email)


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('users.id'))
    plan = Column(Integer, ForeignKey('plans.id'))
    errored = Column(Boolean)
    finished = Column(Boolean)
    timed_out = Column(Boolean)

    def __init__(self, user, plan):
        self.user = user
        self.plan = plan

    def set_finished(self, timed_out=False):
        self.finished = True
        self.timed_out = timed_out

    def __repr__(self):
        return "<Task: %d: (%d %d) running: %s(%s)>" % (id,
                                                        self.user,
                                                        self.plan,
                                                        self.finished,
                                                        self.timed_out)
