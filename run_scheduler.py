#!/bin/python3
# Python3

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from time import sleep

from core import task, program, scheduler

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import exists

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql.expression import Select, select
# import sqlalchemy.sql.expression

engine = create_engine('sqlite:////tmp/db/webpy.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

### Models
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

class RequestHandler(SimpleXMLRPCRequestHandler): # Limit to a path
    rpc_paths = ('/RPC2',)


# The scheduling RPC server
class SchedServer(object):
    def __init__(self, ip="localhost", port=8000):
        self.sched = scheduler.Scheduler()
        self.server = SimpleXMLRPCServer((ip, port),
                                         requestHandler=RequestHandler)
        self.server.register_introspection_functions()
        self.serving = 0
        self.server.register_function(self.push)
        self.server.register_function(self.shutdown)
        self.sched.run()
        self.server.serve_forever()

    def push(self, username, policy_number, code):
        user_id = db_session.query(User.id).filter(User.username == username).one()[0]
        db_task = Task(user_id, policy_number)
        t = task.Task(program.Program(code), username, 3, 1000)
        index = self.sched.add(t)
        db_session.add(db_task)
        db_session.commit()
        if index == -1:
            print("Shutting down")
            return -1
        ret_val = self.sched.get(index)
        while ret_val is None:
            ret_val = self.sched.get(index)
            sleep(0.2)
        return ret_val

    def shutdown(self):
        self.sched.join()

s = SchedServer("localhost", 8000)
