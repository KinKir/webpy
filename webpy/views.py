from webpy import app
from webpy.user_manager import user_exists, add_user

from flask import render_template, request, redirect, url_for, session

import xmlrpc.client

@app.route('/logout')
def logout():
    if 'username' not in session:
        return redirect(url_for('index'))
    print("logging out %s" % (session['username']))
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))
    else:
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            form_username = request.form['username']
            form_email = request.form['email']
            print("Searching for:", form_username, ":", form_email)
            if user_exists(form_username, form_email):
                print("Found")
                session['username'] = form_username
                return redirect(url_for('index'))
            else:
                print("Not found, creating user")
                add_user(form_username, form_email)
                session['username'] = form_username
                return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        if 'username' not in session:
            return redirect(url_for('login'))
        print('User request: %s' % session['username'])
        return render_template('index.html')
    elif request.method == 'POST':
        program = request.form['program']
        server = xmlrpc.client.ServerProxy('http://localhost:8000')
        output = server.push(session['username'], 1, program)
        return render_template('index.html', program=program, output=output)
