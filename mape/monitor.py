from mape.database import db_session, func
from mape.models import Task


# An interface between the database and the rest of the loop
# Monitor plans users are using
class Monitor(object):
    # Count the number of registerd tasks
    def total_tasks(self):
        return db_session.query(func.count(Task.id)).one()[0]

    # Gets the count for all plans
    # Returns in the form:
    # (task plan id, count)
    def tasks(self):
        return db_session.query(Task.plan,
                                func.count(Task.id)).group_by(Task.plan).all()
