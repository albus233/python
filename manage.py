from __future__ import with_statement
from flask.ext.script import Manager
from flask import Flask

from flaskr import User, db

app = Flask(__name__)
manager = Manager(app)
DEBUG = True
SECRET_KEY = 'albus233'
SQLALCHEMY_DATABASE_URI = 'sqlite:///flaskr.db'


@manager.option('-n', '--name', help='The username you want to register')
@manager.option('-p', '--password', help='The password for this user')
def add(name, password):
    print "Name:", name, "password:", password
    u = User.query.filter_by(username=name).first()
    if u is None:
        user = User(name, password)
        db.session.add(user)
        db.session.commit()
        print 'Add success!'


@manager.option('-n', '--name', help='Your name')
@manager.option('-p', '--password', help='Your new password')
def change(name, password):
    print "Name:", name, "New password:", password
    u = User.query.filter_by(username=name).first()
    user = User(name, password)
    db.session.delete(u)
    db.session.add(user)
    db.session.commit()
    print 'Change password success!'


@manager.option('-n', '--name', help='The username you want to delete')
def delete(name):
    print "Name:", name
    u = User.query.filter_by(username=name).first()
    db.session.delete(u)
    db.session.commit()
    print 'Delete success!'

if __name__ == "__main__":
    manager.run()
