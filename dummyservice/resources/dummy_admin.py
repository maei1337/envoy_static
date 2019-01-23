from flask_restful import Resource
from schema.dummy import DummySchema
from models.dummy import DummyModel
from marshmallow import ValidationError
from flask import request
from flask_jwt_extended import (jwt_refresh_token_required,
                                get_jwt_identity,
                                get_jwt_claims,
                                jwt_required,
                                get_raw_jwt
                                )

############################
### Marshmallow Schema init
############################
dummy_schema = DummySchema()
dummy_schema_list = DummySchema(many=True)


class Dummy(Resource):
############################
### GET entry depend on user-identity
############################
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()

        dummy = DummyModel.find_by_userid(user_id)

        if dummy:
            return {'message': dummy_schema_list.dump(DummyModel.query.filter_by(user_id=user_id))}, 200
        return {'message': 'No Data found'}, 400
