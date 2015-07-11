from webpy import app
from webpy.user_manager import user_exists, add_user
import webpy.models

from sqlalchemy.sql import exists

from webpy.database import db_session

from flask import render_template, request, redirect, url_for, session, flash

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
        flash("You were automatically logged out")
        return redirect(url_for('index'))
    else:
        if request.method == 'GET':
            plans = webpy.models.Plan.query.all()
            return render_template('login.html', plans=plans)
        elif request.method == 'POST':
            form_username = request.form['username']
            form_email = request.form['email']
            form_plan = request.form['plan']
            print("Form Plan:", form_plan)
            session['plan'] = form_plan
            if user_exists(form_username, form_email):
                session['username'] = form_username
                return redirect(url_for('index'))
            else:
                add_user(form_username, form_email)
                session['username'] = form_username
                return redirect(url_for('index'))


@app.route('/admin', methods=["GET", "POST"])
def administer():
    if 'username' not in session:
        flash("You were automatically logged out")
        return redirect(url_for('login'))
    if request.method == 'POST':
        selected_plan = request.form['plan']
        try:
            account_policy = db_session.query(webpy.models.Account_Policies).first()
            account_policy.maxmize_plan = selected_plan
        except:
           account_policy = webpy.models.Account_Policies(selected_plan)
           db_session.add(account_policy)
        db_session.commit()
        return redirect(url_for('index'))
    else:
        selected_plan = 0
        try:
            selected_plan = db_session.query(webpy.models.Account_Policies).first().maxmize_plan
        except:
            pass

        plans = webpy.models.Plan.query.all()
        return render_template('admin.html', plans=plans, selected_plan=selected_plan)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        if 'username' not in session:
            return redirect(url_for('login'))
        try:
            pass
        except KeyError:
            flash("You were automatically logged out")
            return redirect(url_for('login'))
        return render_template('index.html')
    elif request.method == 'POST':
        try:
            program = request.form['program']
            server = xmlrpc.client.ServerProxy('http://localhost:8000')
            print("form plan sending:", session['plan'])
            output = server.push(session['username'], session['plan'], program)
            return render_template('index.html', program=program, output=output)
        except KeyError:
            flash("You were automatically logged out")
            return redirect(url_for('login'))
