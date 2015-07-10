from time import sleep
import math
import os

import threading
import task


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

                print("Running task at index: {0}".format(item_index))
                print("Running Task for user: {0}".format(t.username))
                print("Output index:", output_index)
                t.run()
                sleep(t.time_slice / 1000)
                done = False
                t.time -= 1
                if not t.alive:
                    done = True
                    print("Done")
                t.stop()

                if done:
                    self.output[output_index] = t.output
                elif not t.time:
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

        print("adding:", self.queue)
        self.queue.append((t, index))
        print("adding:", self.queue)
        print("Adding item at queue:output {0}:{1}".format(len(self.queue) - 1, index))
        return index

    def get(self, index):
        # if it is None, the cell is not in use
        # if it is the task, then the process hasn't finished yet

        if self.output[index] is None or self.output[index] is 1:
            print("No output yet")
            return None
        else:
            print("Output found")
            print(self.output, ":", index)
            print("The output:", self.output[index])
            ret_val = self.output[index]
            self.output[index] = None
            print("Return value:", ret_val)
            return ret_val

    def run(self):  # Starts the whole system in motion
        self.runner.start()

    def stop(self):  # Kills self
        self.die = True
        self.runner.join()

    def join(self):  # Wait for all processes to stop before killing self
        self.f_join = True
        self.runner.join()
