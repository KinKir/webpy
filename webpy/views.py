from webpy import app
from webpy.user_manager import user_exists

from flask import render_template, request, redirect, url_for


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        print("Searching for:", username, ":", email)
        print(user_exists(username, email))
        # Check that user exists and log them in if they exist
        return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        output = request.form['program']
        program = output
        print(output)
        return render_template('index.html', program=program, output=output)
