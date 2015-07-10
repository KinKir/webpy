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
        self.program.run()

    def kill(self):
        self.program.kill()

    def stop(self):
        self.program.stop()

    @property
    def alive(self):
        return self.program.alive

    @property
    def output(self):
        return self.program.get_output()
