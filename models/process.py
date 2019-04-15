from typing import Dict, List, Union

from db import db

ProcessJSON = Dict[str, Union[int, str, float]]

class ProcessModel(db.Model):
    __tablename__ = 'processes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    progress = db.Column(db.Float(precision=2))

    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'))


    def __init__(self, name: str, progress: int, agent_id: int):
        self.name = name
        self.progress = progress
        self.agent_id = agent_id

    def json(self) -> ProcessJSON:
        return {
            'id': self.id,
            'name': self.name,
            'progress': self.progress,
            'agent_id': self.agent_id
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