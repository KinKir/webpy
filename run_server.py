#!/bin/python3
# Python3

DEBUG = True
IP_ADDRESS = '0.0.0.0'  # Accept all IP addresses, use localhost:8080
PORT_NUMBER = 8080
THREADED = False  # False for now, will change on release

from webpy import app
app.run(host=IP_ADDRESS, port=PORT_NUMBER, debug=DEBUG, threaded=THREADED)
