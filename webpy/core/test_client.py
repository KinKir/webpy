import xmlrpc.client

code1 = \
    """
print('This was a triumph')
"""
code2 = "print('Im making a note here, HUGE success.')"
code3 = "print('Its hard to overstate my satisfaction.')"
code4 = \
    """
def main(s):
    print(s)
    a = 10
    b = 20
    print("Addition: a+b", a + b)
    print("Modulus: a%s", a % 2)

# main("Hello World")
# Test stderr
main("a:", 10, "b:", 20)
"""

code5 = \
    """
def heavy():
    while True:
        pass

heavy()
"""

server = xmlrpc.client.ServerProxy('http://localhost:8000')
ev_req = server.push("Evan", 1, code1)
print(ev_req, end="")
nav_req = server.push("Nav", 2, code2)
print(nav_req, end="")
sean_req = server.push("Sean", 3, code3)
print(sean_req, end="")
ev_req = server.push("Evan", 1, code4)
print(ev_req, end="")
nav_req = server.push("Nav", 2, code5)
print(nav_req, end="")

print()
