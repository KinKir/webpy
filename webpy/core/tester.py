import task
import scheduler


def main():
    code1 = "Hello World"
    code2 = "Goodbye Crule World"
    code3 = "Sup"

    t1 = task.Task(code1, "Evan", 3, 1000)  # Gold
    t2 = task.Task(code2, "Nav", 2, 500)  # Silver
    t3 = task.Task(code3, "Sean", 1, 250)  # Bronze

    sched = scheduler.Scheduler()
    print(type(sched))
    sched.add(t1)
    sched.add(t2)
    sched.add(t3)
    sched.run()
    sched.add(t1)
    sched.add(t2)
    sched.add(t3)
    print(type(sched))
    sched.join()

if __name__ == "__main__":
    main()
