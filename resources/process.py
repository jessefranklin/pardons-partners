import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.process import ProcessModel

class ProcessList(Resource):
    def get(self):
        return {'processes': list(map(lambda x: x.json(), ProcessModel.query.all()))}


class Process(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('progress',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('agent_id',
                       type=int,
                       required=True,
                       help="Every progress needs an agent id"
                       )

    @jwt_required()
    def get(self, name):
        process = ProcessModel.find_by_name(name)
        if process:
            return process.json()
        return {'message': 'process not found'}, 404

    def post(self, name):

        if ProcessModel.find_by_name(name):
            return {'message': "an item with name {} already exists".format(name)}, 400

        data = Process.parser.parse_args()

        process = ProcessModel(name, **data)

        try:
            process.save_to_db()
        except:
            return {"message": "an error occurred"}

        return process.json(), 201

    def delete(self, name):
        process = ProcessModel.find_by_name(name)
        if process:
            process.delete_from_db()

        return {'message': 'item deleted'}

    def put(self, name):
        data = Process.parser.parse_args()
        process = ProcessModel.find_by_name(name)

        if process:
            process.progress = data['progress']
        else:
            process = ProcessModel(name, **data)

        process.save_to_db()

        return process.json()
