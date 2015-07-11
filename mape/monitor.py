from mape.database import db_session, func
from mape.models import Task, Account_Policies, Plan


# An interface between the database and the rest of the loop
# Monitor plans users are using
class Monitor(object):

    def get_plan(self):
        try:
            return db_session.query(Account_Policies).first().maxmize_plan
        except:
            return -1

    def get_plan_count(self):
        plan = self.get_plan()
        if plan == -1:
            return 0
        return self.task_count(plan)


    # Count the number of registered tasks
    def total_tasks(self):
        return db_session.query(func.count(Task.id)).one()[0]

    # Gets the count for all plans
    # Returns in the form:
    # (task plan id, count)
    def tasks(self):
        return db_session.query(Task.plan,
                                func.count(Task.id)).group_by(Task.plan).all()

    # Gets the number of tasks for a given plan
    def task_count(self, task_number):
        return db_session.query(
            func.count(Task.id)).filter(Task.plan == task_number).one()[0]
