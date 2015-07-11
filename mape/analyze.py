class Analyer(object):
    def analyze(self, plan_count, total_tasks, task_breakdown):
        if plan_count < 0:
            return 0
        # get the plan from database
        if total_tasks < 10:  # Too few to do anything with
            return 0

        ret_list = []

        for obj in task_breakdown:
            if obj[1] == plan_count:
                ret_list.append((obj[0], 0))
                continue

            val = plan_count - obj[1]
            val = val - (total_tasks // 10)
            ret_list.append((obj[0], -val))
        return ret_list
