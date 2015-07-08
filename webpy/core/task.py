# Contains metadata for each program
class Task(object):
    def __init__(self, program, username, time, quota):
        self.program = program
        self.username = username
        self.time = time  # Number of iterations
        self.time_slice = quota  # Length of iteration
        self.retval = 0

    def __len__(self):
        return len(self.program)

    def run(self):
        if self.time == 0:  # If we can't be run anymore
            self.retval = 1
            self.program.kill()
            return self.retval
        self.program.run()

    def kill(self):


    def stop(self):
        self.program.stop()
