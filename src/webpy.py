from flask import Flask

DEBUG = True
SECRET_KEY = ''
IP_ADDRESS = '127.0.0.1'
PORT_NUMBER = 8080
PROCESSES = 3

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def main():
    return 'Hello World'

if __name__ == '__main__':
    app.run(host=IP_ADDRESS, port=PORT_NUMBER, debug=DEBUG, processes=PROCESSES)
