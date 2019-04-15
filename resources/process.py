from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required
)
from models.process import ProcessModel


class ProcessList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        proccesses =  [x.json() for x in ProcessModel.find_all()]
        if user_id:
            return {'processes': proccesses}, 200

        return {'processes': [x['name'] for x in proccesses],
                'message': 'More data available for logged in users'
                },200


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

    @jwt_required
    def get(self, name: str):
        process = ProcessModel.find_by_name(name)
        if process:
            return process.json()
        return {'message': 'process not found'}, 404

    @fresh_jwt_required
    def post(self, name: str):

        if ProcessModel.find_by_name(name):
            return {'message': "an item with name {} already exists".format(name)}, 400

        data = Process.parser.parse_args()
        print(data['progress'])
        process = ProcessModel(name, **data)

        try:
            process.save_to_db()
        except:
            return {"message": "an error occurred"}

        return process.json(), 201

    @jwt_required
    def delete(self, name: str):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privlages required.'}, 401
        process = ProcessModel.find_by_name(name)
        if process:
            process.delete_from_db()
            return {'message': 'item deleted'}
        return {'message': 'item not found'}, 404

    def put(self, name: str):
        data = Process.parser.parse_args()
        process = ProcessModel.find_by_name(name)

        if process:
            process.progress = data['progress']
        else:
            process = ProcessModel(name, **data)

        process.save_to_db()

        return process.json()
