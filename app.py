from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskr.db'
db = SQLAlchemy(app)


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
