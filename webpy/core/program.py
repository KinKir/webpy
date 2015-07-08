from multiprocessing import Process, Pipe
# import os
import sys


# conn, the connection with the parent
# code, the python code to be interpreted
def interpret(conn, code):
    output = sys.stdout
    print("hello")
    print(code)
    conn.send([output, 0])
    conn.close()


# Smallest unit
class Program(object):
    def __init__(self, code):
        self.prog = code
        self.length = len(code)  # Cache it, it doesn't change -- Lines of code
        self.parent_conn, self.child_conn = Pipe()
        self.proc = Process(target=interpret(code),
                            args=(self.child_conn, code,))

    def __len__(self):
        return self.length

    def run(self):  # continues the program
        # send SIGCONT
        pass

    def kill(self):
        # kill the process
        pass

    def stop(self):  # Pauses the program
        # send SIGSTOP to process
        pass


if __name__ == '__main__':
    test_code = \
"""
def main():
    print("Hello")
main()
"""
    test_prog = Program
