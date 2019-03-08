import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import (
    UserRegister,
    User,
    UserLogin,
    UserLogout,
    TokenRefresh,
    UserConfirm
)
from resources.process import Process, ProcessList
from resources.agent import Agent, AgentList
from resources.confirmation import Confirmation, ConfirmationByUser

from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///client.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access','refresh']
app.secret_key =  os.environ.get('SECRET_KEY')
api = Api(app)

jwt = JWTManager(app)

@app.before_first_request
def create_tables():
    db.create_all()

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
            return {'is_admin': True}
    return {'is_admin': False}

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired',
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed',
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def unauthorized_loader_token_callback(error):
    return jsonify({
        'description': 'Request does not contain access token',
        'error': 'invalid_token'
    }), 401

@jwt.needs_fresh_token_loader
def needs_fresh_token_callback(error):
    return jsonify({
        'description': 'The token is not fresh',
        'error': 'fresh_token_required'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": 'The token has been revoked',
        "error": 'revoked_token'
    }), 401

api.add_resource(Agent, '/agent/<string:name>')
api.add_resource(AgentList, '/agents')
api.add_resource(ProcessList, '/processes')
api.add_resource(Process, '/process/<string:name>')

api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')

api.add_resource(UserConfirm, '/user_confirm/<int:user_id>')

api.add_resource(Confirmation, "/user_confirm/<string:confirmation_id>")
# api.add_resource(ConfirmationByUser, "/confirmation/user/<int:user_id>")

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)