from multiprocessing import Process, Pipe
# import os
import sys
import psutil

import io
from contextlib import redirect_stdout


# conn, the connection with the parent
# code, the python code to be interpreted
def interpret(conn, code):
    output = ""
    with io.StringIO() as buf, redirect_stdout(buf):
        # does not destroy scope, so you can destroy the server if you name your
        # variables wrong (or right if you are malicious)
        exec(code)

        #############################################
        # Run script sandboxed...
        # Sandboxing is actually really difficult...
        #############################################
        output = buf.getvalue()
    conn.send(output)
    conn.close()


# Smallest unit
class Program(object):
    def __init__(self, code):
        self.prog = code
        self.length = len(code)  # Cache it, it doesn't change -- Lines of code
        self.parent_conn, self.child_conn = Pipe(True)
        self.started = False
        self.proc = Process(target=interpret,
                            args=(self.child_conn, code,))
        self.proc_pid = 0
        self.output = ""

    def __len__(self):
        return self.length

    def run(self):  # continues the program
        # We need to start the process before we could possibly continue
        if not self.started:
            self.proc.start()
            self.proc_pid = self.proc.pid
            print("process pid:", self.proc_pid)
        elif self.alive:
            p = psutil.Process(self.proc_pid)
            p.resume()

        self.started = True
        print("Running program!")

    def kill(self):
        # kill the process
        self.proc.terminate()
        self.proc.join()
        return self.proc.exitcode

    def stop(self):  # Pauses the program
        self.output = self.parent_conn.recv()
        if not self.alive:
            self.proc.join()
            return self.proc.exitcode
        p = psutil.Process(self.proc_pid)
        p.suspend()
        # send SIGSTOP to process

    def get_output(self):
        return self.output

    @property
    def alive(self):
        return self.proc.is_alive()

from time import sleep

if __name__ == '__main__':
    blob = "aperture science"
    bad_exec = "we do what we must, because we can."
    test_code = """
def main():
    print(blob)
    print(bad_exec)

print("This was a triumph, I'm making a note here, huge success")
print("It's hard to over state my satisfaction")
main()
"""
    test_prog = Program(test_code)
    test_prog.run()
    while test_prog.alive:
        print("I'm still alive")
        sleep(0.2)
    print("Return code:", test_prog.stop())
    print(test_prog.get_output())
