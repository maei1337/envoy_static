from flask_restful import Resource, reqparse, inputs
from models.dummy import DummyModel
from flask_jwt_extended import (jwt_refresh_token_required,
                                get_jwt_identity,
                                get_jwt_claims,
                                jwt_required,
                                get_raw_jwt
                                )

class Dummy(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()

        if DummyModel.find_by_userid(user_id):
            return {'message': [data.json() for data in DummyModel.query.filter_by(user_id=user_id)]}, 200

        return {'message': 'No Data'}, 400

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('string', type=str, required=True, help="This field not left blank")
        parser.add_argument('int_zahl', type=int, required=True, help="This field not left blank")
        parser.add_argument('float_zahl', type=float, required=True, help="This field not left blank")
        parser.add_argument('bool', type=inputs.boolean, required=True, help="This field not left blank")
        parser.add_argument('text', type=str, required=True, help="This field not left blank")

        data = parser.parse_args()
        user_id = get_jwt_identity()

        if DummyModel.find_by_string(data['string']):
            return {'message': '"String" already exist'}, 400

        product = DummyModel(user_id, **data)
        product.save_to_db()

        return product.json(), 200

    @jwt_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help="ID field not left blank")
        parser.add_argument('string', type=str)
        parser.add_argument('int_zahl', type=int)
        parser.add_argument('float_zahl', type=float)
        parser.add_argument('bool', type=inputs.boolean)
        parser.add_argument('text', type=str)

        data = parser.parse_args()
        user_id = get_jwt_identity()

        # select user_id und dann schauen, ob angegebene id zu user_id stimmt!!

        if DummyModel.find_by_id(data['id']):
            return {'message': '"String" already exist'}, 400

        product = DummyModel(user_id, **data)
        product.save_to_db()

        return product.json(), 200

class DummyList(Resource):
    @jwt_required
    def get(self):
        return {'data': [dummy.json() for dummy in DummyModel.query.all()]}, 200
