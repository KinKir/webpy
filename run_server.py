#!/bin/python3
# Python3

DEBUG = True
IP_ADDRESS = '0.0.0.0'  # Accept all IP addresses, use localhost:8080
PORT_NUMBER = 8080
THREADED = False  # False for now, will change on release
SECRET_KEY = 'webpysecret111'  # This is the worst secret ever

from webpy import app
app.secret_key = SECRET_KEY
app.run(host=IP_ADDRESS, port=PORT_NUMBER, debug=DEBUG, threaded=THREADED)
