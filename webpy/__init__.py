from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

import webpy.views

from webpy.database import db_session
from webpy.database import init_db

@app.before_request
def start_session():
    init_db()

# @app.teardown_appcontext
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
