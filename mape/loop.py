from mape.database import db_session
from mape.models import Account_Policies

from mape.monitor import Monitor
from mape.analyze import Analyer
from mape.plan import Planner

from time import sleep


class MAPELoop(object):
    monitor = None
    analyzer = None
    planner = None
    optimize_plan = 0

    def __init__(self):
        self.monitor = Monitor()
        self.analyzer = Analyer()
        self.planner = Planner()
        self.optimize_plan = db_session.query(Account_Policies).first()

    def run(self):
        while True:
            total_tasks = self.monitor.total_tasks()
            task_breakdown = self.monitor.tasks()
            plan_count = self.monitor.get_plan_count()
            analysis = self.analyzer.analyze(plan_count, total_tasks, task_breakdown)
            if type(analysis) is list:
                self.planner.plan_and_execute(analysis)
            sleep(2)


if __name__ == "__main__":
    m = MAPELoop()
    m.run()
