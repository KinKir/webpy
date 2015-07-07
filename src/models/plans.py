from sqlalchemy import Column, Integer, String
from webpy.database import Base



class Plan():
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    cpu_time = db.Column(db.Integer)
    cpu_quota = db.Column(db.Integer)

    def __init__(self, name, time, quota):
        self.name = name
        self.time = time
        self.quota = quota


