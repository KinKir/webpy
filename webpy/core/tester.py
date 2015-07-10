import program
import task
import scheduler

from time import sleep


def main():
    code1 = "print('Hello World')"
    code2 = "print('Goodbye Cruel World')"
    code3 = "print('Sup')"

    t1 = task.Task(program.Program(code1), "Evan", 3, 1000)  # Gold
    t2 = task.Task(program.Program(code2), "Nav", 2, 500)  # Silver
    t3 = task.Task(program.Program(code3), "Sean", 1, 250)  # Bronze

    sched = scheduler.Scheduler()
    sched.run()
    sleep(1)
    sched.add(t1)
    sleep(0.25)
    sched.add(t2)
    sleep(0.5)
    sched.add(t3)
    sched.join()

if __name__ == "__main__":
    main()
