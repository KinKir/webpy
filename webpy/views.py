from webpy import app
from flask import render_template

@app.route('/')
def index():
    Input = "#Input your Python Program here"
    Output = "Python Output Area"
    return render_template('index.html', PyOutput = Output, PyInput=Input)
