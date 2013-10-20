from __future__ import with_statement
from contextlib import closing
import sqlite3
from sqlite3 import *
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from sqlalchemy import *
from datetime import *
from sqlalchemy.orm import *
from flask.ext.superadmin import *
from flask.ext.sqlalchemy import *

from app import app, db, User, entries, create

DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

create()

@app.route('/')
def show_entries():
    cur = db.session.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    t = entries(request.form['title'], request.form['text'])
    db.session.add(t)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

    
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':    
        username = request.form["username"]
        password = request.form["password"]  
        u = User.query.filter_by(username=username).first_or_404()
        if u.password == password:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/rr')
def rr():
    error = None
    return render_template('register.html', error=error)

@app.route('/register', methods=['GET','POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['repeatpassword']
        if repassword == password:
            t1 = User(username, password)
            db.session.add(t1)
            db.session.commit()
            flash('Register successfully!')
            return redirect(url_for('login'))
        else:
            flash('password is not same')
            return redirect(url_for('rr'))
    return render_template('register.html', error=error)
    
if __name__ == '__main__':
    app.run(debug=True)
