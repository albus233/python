from sqlalchemy import *
from datetime import *
from sqlalchemy.orm import *

engine = create_engine("sqlite:///flaskr.db", echo=True)
entries = MetaData()
users = Table('users', entries,
              Column('id', Integer, primary_key=True),
              Column('title', String(40), nullable = False),
              Column('text', String, nullable = False))
entries.create_all(engine)
class user(object):
    def __int__(self, title, text):
        self.title = title
        self.text = text
mapper(user, users)
Session = sessionmaker(bind = engine)
session = Session()
session.commit()
