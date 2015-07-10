from time import sleep
import math
import os

import threading
import core.task


class Scheduler(object):
    def __init__(self):
        self.queue = []         # tasks to be run
        self.output = []
        self.die = False        # Kills threads
        self.f_join = False
        self.runner = threading.Thread(target=self._proc)
        self.stopped = True

    @property
    def empty(self):
        return len(self.queue) == 0

    # Does the actual heavy lifting for the scheduler
    def _proc(self):
        self.stopped = False
        while True:
            # Block if there are no tasks to be run
            # TODO: Get rid of the freaking spin lock
            while not self.queue:
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

                t, output_index = self.queue.pop(item_index)
                print("Running Task for user: {0}".format(t.username))
                t.run()
                sleep(t.time_slice / 1000)
                done = False
                t.time -= 1
                print("Remaining time:", t.time * t.time_slice / 1000)
                if not t.alive:
                    done = True
                t.stop()
                if done:
                    self.output[output_index] = t.output
                elif t.time <= 0:
                    t.kill()
                    self.output[output_index] = "Error: timed out"
                else:
                    self.queue.append((t, output_index))

            except IndexError:
                # If this occurs, there was some sort of weird slip.
                # The system will still be fine though and should sleep on
                # the next iteration
                pass

    def add(self, t):
        if self.f_join or self.die:
            return -1
        try:
            index = self.output.index(None)
            self.output[index] = 1
        except:
            index = len(self.output)
            self.output.append(1)
        self.queue.append((t, index))
        return index

    def get(self, index):
        # if it is None, the cell is not in use
        # if it is the task, then the process hasn't finished yet
        if self.output[index] is None or self.output[index] is 1:
            return None
        else:
            ret_val = self.output[index]
            self.output[index] = None
            return ret_val

    def run(self):  # Starts the whole system in motion
        self.runner.start()

    def stop(self):  # Kills self
        self.die = True
        self.runner.join()

    def join(self):  # Wait for all processes to stop before killing self
        self.f_join = True
        self.runner.join()
