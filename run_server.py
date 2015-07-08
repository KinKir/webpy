#!/bin/python3
# Python3

import os

DEBUG = True
IP_ADDRESS = '0.0.0.0'  # Accept all IP addresses, use localhost:8080
PORT_NUMBER = 8080
THREADED = False  # False for now, will change on release
SECRET_KEY = os.urandom(24)

from webpy import app
app.secret_key = SECRET_KEY
app.run(host=IP_ADDRESS, port=PORT_NUMBER, debug=DEBUG, threaded=THREADED)
