from mape.database import db_session
from mape.models import Plan


class Planner(object):
    def plan_and_execute(self, analysis):
        for diff in analysis:
            update_plan = db_session.query(Plan).filter(Plan.id == diff[0]).one()
            # print("Plan:", diff)
            # Low demand, lower price
            if diff[1] < 0:
                if (update_plan.price > 2):
                    update_plan.price += diff[1] // 10
                db_session.commit()
            # High demand, higher price
            elif diff[1] > 0:
                update_plan.price += diff[1] // 10
                db_session.commit()
