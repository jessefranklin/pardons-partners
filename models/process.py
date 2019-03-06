from db import db

class ProcessModel(db.Model):
    __tablename__ = 'processes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    progress = db.Column(db.Float(precision=2))

    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'))
    agent = db.relationship('AgentModel')


    def __init__(self, name, progress, agent_id):
        self.name = name
        self.progress = progress
        self.agent_id = agent_id

    def json(self):
        return {'name': self.name, 'progress': self.progress}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()