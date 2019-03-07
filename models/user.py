from flask import request, url_for
from requests import Response
from db import db

from libs.mailgun import Mailgun


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(80), nullable=False, unique=True)
    activated = db.Column(db.Boolean, default=False)

    def __init__(self, username: str, password: str, email: str, activated: bool):
        self.username = username
        self.password = password
        self.email = email
        self.activated = activated

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'activated': self.activated
        }

    @classmethod
    def find_by_username(cls, username: str):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    def send_confirmation_email(self) -> Response:
        link = request.url_root[:-1] + url_for("userconfirm", user_id=self.id)
        subject = "Registration confimration"
        text = f"Please click the link to confirm your registration link {link}"
        html = f'<html>Please click the link to confirm your registration <a href="{link}">{link}</a> </html>'

        return Mailgun.send_email([self.email], subject, text, html)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()