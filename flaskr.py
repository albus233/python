from __future__ import with_statement
from flask import request, session, redirect, url_for, abort
from flask import render_template, flash

from app import app, db, User, Entries, create

DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'

app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

create()
user = 'None'


@app.route('/')
def index():
    global user
    session.pop('logged_in', None)
    user = 'None'
    cur = db.session.execute('select title, text from\
                             Entries order by id desc')
    entriess = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', Entries=entriess)


@app.route('/show')
def show_entries():
    cur = db.session.execute('select title, text from\
                             Entries order by id desc')
    entriess = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', Entries=entriess)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    t = Entries(request.form['title'], request.form['text'], user)
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
            global user
            user = username
            flash('You were logged in!')
            flash(user)
            return redirect(url_for('show_entries'))
        else:
            flash('Wrong password')
            return redirect(url_for('login'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    global user
    session.pop('logged_in', None)
    user = 'None'
    flash('You were logged out')
    return redirect(url_for('show_entries'))


@app.route('/delete', methods=['POST'])
def delete():
    tit = request.form["delete"]
    owner = entries.query.filter_by(title=tit).first()
    if user == 'admin':
        db.session.delete(owner)
        db.session.commit()
    elif user == owner.publisher:
        db.session.delete(owner)
        db.session.commit()
    else:
        flash('You don\' have permission for this')
    return redirect(url_for('show_entries'))


@app.route('/rr')
def rr():
    error = None
    return render_template('register.html', error=error)


@app.route('/r')
def r():
    error = None
    return render_template('repwd.html', error=error)


@app.route('/repwd', methods=['POST'])
def repwd():
    global user
    if not session.get('logged_in'):
        abort(401)
    else:
        password = request.form["password"]
        u = User.query.filter_by(username=user).first_or_404()
        db.session.delete(u)
        db.session.commit()
        u = User(user, password)
        db.session.add(u)
        db.session.commit()
        session.pop('logged_in', None)
        user = 'None'
        flash('Success!')
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['repeatpassword']
        if repassword == password:
            u = User.query.filter_by(username=username).first()
            if username == 'None':
                flash('You can\'t use this id')
                return redirect(url_for('rr'))
            if u is None:
                t1 = User(username, password)
                db.session.add(t1)
                db.session.commit()
                flash('Register successfully!')
                return redirect(url_for('login'))
            else:
                flash('The username has been registed')
                return redirect(url_for('rr'))
        else:
            flash('password is not same')
            return redirect(url_for('rr'))
    return render_template('register.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)
