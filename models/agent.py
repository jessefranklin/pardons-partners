from typing import Dict, List

from db import db

class AgentModel(db.Model):
    __tablename__ = 'agents'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    processes = db.relationship('ProcessModel', lazy='dynamic')

    def __init__(self, name: str):
        self.name = name

    def json(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'processes': [process.json() for process in self.processes.all()]
        }

    @classmethod
    def find_all(cls) -> List:
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()