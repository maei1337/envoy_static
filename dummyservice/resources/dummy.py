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

        if DummyModel.find_by_userid(user_id):
            return {'message': dummy_schema_list.dump(DummyModel.query.filter_by(user_id=user_id))}, 200
        return {'message': 'No Data found'}, 400

############################
### POST new entry depend on user-identity
############################
    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        dummy_json = request.get_json()
        dummy_json["user_id"]=user_id

        try:
            dummy_data = dummy_schema.load(dummy_json)
        except ValidationError as err:
            return err.messages, 400

        if DummyModel.find_by_string(dummy_data.string):
            return {'message': '"String" already exist'}, 400

        dummy_data.save_to_db()

        return {'message': dummy_schema.dump(dummy_data)}, 200

############################
### UPDATE a existing entry depend on user-identity
############################
    @jwt_required
    def put(self):
        dummy_json = request.get_json()
        user_id = get_jwt_identity()
        dummy_json["user_id"]=user_id
        dummy_json["string"]=string
        dummy_json["float_zahl"]=float
        dummy_json["bool"]=bool
        dummy_json["int_zahl"]=int
        dummy_json["id"]=id

        change_dummy = DummyModel.query.filter_by(id=dummy_json["id"]).first()

        # Abfangen wenn es ID nicht gibt des dummy
        if change_dummy is None or change_dummy.user_id != user_id:
            return {'message': 'No right credintials to change'}, 400

        try:
            dummy_data = dummy_schema.load(dummy_json)
        except ValidationError as err:
            return err.messages, 400

        # if DummyModel.find_by_string(dummy_data.string):
        #     return {'message': '"String" already exist'}, 400

        #dummy_data.save_to_db()
        #
        #return {'message': dummy_schema.dump(dummy_data)}, 200

class DummyList(Resource):
############################
### GET all Entries
############################
    @jwt_required
    def get(self):
        return {'message': dummy_schema_list.dump(DummyModel.query.all())}, 200
