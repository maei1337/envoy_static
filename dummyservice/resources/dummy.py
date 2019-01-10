from flask_restful import Resource, reqparse, inputs
from models.dummy import DummyModel
from flask_jwt_extended import (jwt_refresh_token_required,
                                get_jwt_identity,
                                get_jwt_claims,
                                jwt_required,
                                get_raw_jwt
                                )

class Dummy(Resource):
    def get(self):
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('string', type=str, required=True, help="This field not left blank")
        parser.add_argument('int_zahl', type=int, required=True, help="This field not left blank")
        parser.add_argument('float_zahl', type=float, required=True, help="This field not left blank")
        parser.add_argument('bool', type=inputs.boolean, required=True, help="This field not left blank")
        parser.add_argument('text', type=str, required=True, help="This field not left blank")

        data = parser.parse_args()

        if DummyModel.find_by_string(data['string']):
            return {'message': '"String" already exist'}, 400

        product = DummyModel(**data)
        product.save_to_db()

        return product.json(), 200

    def delete(self):
        pass

    def put(self):
        pass


class DummyList(Resource):
    @jwt_required
    def get(self):
        return {'data': [dummy.json() for dummy in DummyModel.query.all()]}, 200
