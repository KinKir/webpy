from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import task, program, scheduler

# The scheduling RPC server

sched = scheduler.Scheduler()
sched.run()

class RequestHandler(SimpleXMLRPCRequestHandler):
    # Limit to a path
    rpc_paths = ('/RPC2',)

# Create server
server = SimpleXMLRPCServer(("localhost", 8000), requestHandler=RequestHandler)
server.register_introspection_functions()


def push_function(username, policy_number, code):
    # Use the policy number to determine timing information
    t = Task(program.Program(code), username, 3, 1000)
    sched.add(t)

server.register_function(push_function, 'push')

def shutdown_function():
    sched.join()

server.register_function(shutdown_function, 'shutdown')

server.serve_forever()
