from typing import Dict, List

from db import db

class File(db.Model):
    __tableName__ = 'file'

    uuid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True, unique=True)
    path= db.Column(db.String(256), index=True, unique=True)
    profile_id= db.Column(db.Integer, db.ForeignKey('profile.uuid'))

    def __repr__(self):
        return '<File %r>' % self.title


