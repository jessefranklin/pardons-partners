from typing import Dict, List

from db import db

class Profile(db.Model):
    __tableName__ = 'profile'

    uuid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), index=True, unique=True)
    email= db.Column(db.String(256), index=True, unique=True)
    phone= db.Column(db.String(256), index=True)
    files= db.Relationship('File', backref='profile')

    def __repr__(self):
        return '<Profile %r>' % self.username


