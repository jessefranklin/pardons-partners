from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.process import Process, ProcessList
from resources.agent import Agent, AgentList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///client.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = ''
api = Api(app)

jwt = JWT(app, authenticate, identity)

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Agent, '/agent/<string:name>')
api.add_resource(AgentList, '/agents')
api.add_resource(ProcessList, '/processes')
api.add_resource(Process, '/process/<string:name>')

api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)