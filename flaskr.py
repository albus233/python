from __future__ import with_statement
from flask import Flask, request, session, redirect, url_for
from flask import render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy

DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskr.db'
db = SQLAlchemy(app)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    text = db.Column(db.Text, nullable=False)
    publisher = db.Column(db.String(50), nullable=False)

    def __init__(self, title, text, publisher):
        self.title = title
        self.text = text
        self.publisher = publisher

    def __repr__(self):
        return '<entries %r>' % self.title


def create():
    db.create_all()
    if User.query.filter_by(username='admin').first() is None:
        admin = User('admin', 'albus233')
        db.session.add(admin)
    db.session.commit()


create()


@app.route('/')
def index():
    if 'username' in session:
        del session['username']
    entries = Entry.query.all()
    return render_template('show_entries.html', entries=entries)


@app.route('/show')
def show_entries():
    entries = Entry.query.all()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if 'username' not in session:
        return redirect(url_for('login'))
    t = Entry(request.form['title'], request.form['text'], session["username"])
    db.session.add(t)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if 'username' in session:
            del session['username']
        username = request.form["username"]
        password = request.form["password"]
        u = User.query.filter_by(username=username).first_or_404()
        if u.password == password:
            session['username'] = request.form['username']
            flash('You were logged in!')
            return redirect(url_for('show_entries'))
        else:
            flash('Wrong password')
            return redirect(url_for('login'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    if 'username' in session:
        del session['username']
    flash('You were logged out')
    return redirect(url_for('show_entries'))


@app.route('/delete', methods=['POST'])
def delete():
    tit = request.form["delete"]
    owner = Entry.query.filter_by(title=tit).first_or_404()
    if session["username"] == 'admin':
        db.session.delete(owner)
        db.session.commit()
    elif session["username"] == owner.publisher:
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
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        password = request.form["password"]
        u = User.query.filter_by(username=session["username"]).first_or_404()
        db.session.delete(u)
        db.session.commit()
        u = User(session["username"], password)
        db.session.add(u)
        db.session.commit()
        if 'username' in session:
            del session['username']
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
