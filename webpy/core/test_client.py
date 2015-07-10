import xmlrpc.client

import task
import program

code1 = "print('This was a triumph')"
code2 = "print('Im making a note here, HUGE success.')"
code3 = "print('Its hard to overstate my satisfaction.')"

t1 = task.Task(program.Program(code1), "Evan", 3, 1000)  # Gold
t2 = task.Task(program.Program(code2), "Nav", 2, 500)  # Silver
t3 = task.Task(program.Program(code3), "Sean", 1, 250)  # Bronze


server = xmlrpc.client.ServerProxy('http://localhost:8000')
print(server.system.listMethods())
ev_req = server.push("Evan", 1, code1)
print(ev_req, end="")
nav_req = server.push("Nav", 2, code2)
print(nav_req, end="")
sean_req = server.push("Sean", 3, code3)
print(sean_req, end="")

# print(server.push(t1))
# print(server.push(t2))
# print(server.push(t3))
