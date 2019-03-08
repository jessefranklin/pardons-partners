from db import db
from uuid import uuid4
from time import time


CONFIRMATION_EXPIRATION_DELTA = 1800    # 30 mins

class ConfirmationModel(db.Model):
    __tablename__ = 'confirmations'

    id = db.Column(db.String(80), primary_key=True)
    expire_at = db.Column(db.Integer, unique=False)
    confirmed = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel")

    def __init__(self, user_id: int, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.expire_at = int(time()) + CONFIRMATION_EXPIRATION_DELTA
        self.id = uuid4().hex
        self.confirmed = False

    def json(self):
        return {
            'id': self.id,
            'expire_at': self.expire_at,
            'confirmed': self.confirmed,
            'user_id': self.user_id,
            'user': self.user
        }

    @classmethod
    def find_by_id(cls, _id: str) -> "ConfirmationModel":
        return cls.query.filter_by(id=_id).first()

    @property
    def expired(self) -> bool:
        return time() > self.expire_at

    def force_to_expire(self) -> None:
        if not self.expired:
            self.expire_at = int(time())
            self.save_to_db()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()