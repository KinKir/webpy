from flask import Flask
app = Flask(__name__)
import webpy.views

from webpy.database import db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    print("Teardown db_session")
    db_session.remove()
