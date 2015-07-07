from webpy import app

from flask import render_template, request


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        output = request.form['program']
        program = output
        print(output)
        return render_template('index.html', program=program, output=output)
