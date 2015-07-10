from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import task
import program
import scheduler

from time import sleep


class RequestHandler(SimpleXMLRPCRequestHandler):
    # Limit to a path
    rpc_paths = ('/RPC2',)


# The scheduling RPC server


class SchedServer(object):
    def __init__(self, ip="localhost", port=8000):
        self.sched = scheduler.Scheduler()
        self.server = SimpleXMLRPCServer((ip, port),
                                         requestHandler=RequestHandler)
        self.server.register_introspection_functions()
        self.serving = 0
        self.server.register_function(self.push)
        self.server.register_function(self.shutdown)
        self.sched.run()
        self.server.serve_forever()

    def push(self, username, policy_number, code):
        t = task.Task(program.Program(code), username, 3, 1000)
        index = self.sched.add(t)
        print(index)
        if index == -1:
            print("Shutting down")
            return -1
        # Keep the index here for a bit and we will return the processed event
        # Again with the spin locks....
        ret_val = self.sched.get(index)
        while ret_val is None:
            print(ret_val)
            ret_val = self.sched.get(index)
            sleep(0.5)
        return ret_val

    def shutdown(self):
        self.sched.join()

s = SchedServer("localhost", 8000)

# sched = scheduler.Scheduler()
# sched.run()
#
#
# # Create server
# server = SimpleXMLRPCServer(("localhost", 8000),
#                                           requestHandler=RequestHandler)
# server.register_introspection_functions()
#
#
# def push_function(username, policy_number, code):
#     # Use the policy number to determine timing information
#     t = task.Task(program.Program(code), username, 3, 1000)
#     sched.add(t)
#     return serving - 1
#
#
# def shutdown_function():
#     sched.join()
#     return None
#
#
# server.register_function(push_function, 'push')
# server.register_function(shutdown_function, 'shutdown')
# server.serve_forever()
