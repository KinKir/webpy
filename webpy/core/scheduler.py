import program
import task
import threading


class Scheduler(object):
    def __init__(self):
        self.queue = []         # tasks to be run
        self.die = False        # Kills threads
        self.join = False
        self.runner = threading.Thread(target=self._proc)
        self.task_lock = threading.Lock()  # The condition
        self.task_cv = threading.Condition(self.task_lock)
        print("Main Thread:", threading.main_thread())

    # Does the actual heavy lifting for the scheduler
    def _proc(self):
        print("Current Thread:", threading.current_thread(), "main:",
                threading.main_thread())
        if threading.current_thread() is threading.main_thread():
            print("Bad, same processing thread and running thread")
        print("Active threads:", threading.active_count())
        print("proc")
        # Do forever...
        while True:
            print("Forever")
            # Except for when we need to die
            if self.die:
                return

            # Block if there are no tasks to be run
            while not self.queue:
                # If the queue is empty and we are joining, then return not
                # sleep
                if self.join:
                    return
                print("No objects in queue: blocking")
                self.task_cv.acquire()
                self.task_cv.wait()

            # Check if we need to die before actually doing any work
            if self.die:
                return

            # A task is in the queue
            try:
                print("yay, running jobs...")
                # Schedule t
                t = self.queue.pop(0)
                print("Running Task for user: {0}\n Slice: {1}, iterations: {2}\
                      ".format(t.username, t.time_slice, t.time))
                t.time -= 1
                print("Queue Size:", len(self.queue))
            except IndexError:
                print("Something is wrong with this, but it should be okay")

    def add(self, t):
        print("add")
        if self.join:
            return
        # Adds a new object to the
        self.queue.append(t)
        try:
            self.task_cv.release()
            self.task_cv.notify()
        except RuntimeError:
            pass

    def run(self):
        print("Before runner")
        self.runner.start()
        print("Passed runner")

    def stop(self):  # Kills self
        self.die = True
        try:
            self.task_cv.release()
            self.task_cv.notify()
        except RuntimeError:
            pass
        self.runner.join()

    def join(self):  # Wait for all processes to stop before killing self
        print("joining")
        self.join = True
        try:
            self.task_cv.release()
            self.task_cv.notify()
        except RuntimeError:
            pass
        print(type(self.runner))
        self.runner.join()
