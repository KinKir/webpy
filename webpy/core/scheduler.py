from time import sleep
import math
import os
import program
import task
import threading


class Scheduler(object):
    def __init__(self):
        self.queue = []         # tasks to be run
        self.die = False        # Kills threads
        self.f_join = False
        self.runner = threading.Thread(target=self._proc)
        self.task_lock = threading.Lock()
        self.task_cv = threading.Condition(self.task_lock)

        # self.join_lock = threading.Lock()  # Blocks reads and writes to f_join
        # We want a semaphore here. We can read many times until a writer enters

        self.stopped = True

    @property
    def empty(self):
        return len(self.queue) == 0

    # Does the actual heavy lifting for the scheduler
    def _proc(self):
        self.stopped = False
        while True:
            # Block if there are no tasks to be run
            # TODO: Get rid of the freaking spin lock at the most convinient time
            while not self.queue:
                print("Spin Locking...")
                if self.die or self.f_join:
                   self.stopped = True
                   return
                sleep(0.5)
            try:
              queue_len = len(self.queue)
              bits_required = math.ceil(math.log2(queue_len))
              item_index = int.from_bytes(
                  os.urandom(math.ceil(bits_required / 8)),
                  'little') % queue_len
              t = self.queue.pop(item_index)
              print("Running Task for user: {0}".format(t.username))
              t.run()
              sleep(t.time_slice / 1000)
              t.time -= 1
              if t.time:
                  self.queue.append(t)
            except IndexError:
                # If this occurs, there was some sort of weird slip.
                # The system will still be fine though and should sleep on the
                # next iteration
                pass

    def add(self, t):
        if self.f_join:
            return
        self.queue.append(t)

    def run(self):
        self.runner.start()

    def stop(self):  # Kills self
        self.die = True
        # try:
        #     self.task_cv.release()
        #     self.task_cv.notify()
        # except RuntimeError:
        #     pass
        self.runner.join()

    def join(self):  # Wait for all processes to stop before killing self
        self.f_join = True
        # while not self.stopped:
        #     try:
        #         self.task_cv.release()
        #         self.task_cv.notify()
        #     except RuntimeError:
        #         pass
        self.runner.join()
