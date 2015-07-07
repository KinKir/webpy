from sqlalchemy import Column, Integer, String
from webpy.database import Base

# User Class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    plan_id = db.Column(db.Integer) # 0 plan is anon user
    def __init__(self, username, email, plan=0):
        self.username = username
        self.email = email
        self.plan = plan

    def __repr__(self):
        return "<User: %r:%r>" % self.username, self.plan

