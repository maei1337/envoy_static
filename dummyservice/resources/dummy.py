from flask_restful import Resource
from schema.dummy import DummySchema
from models.dummy import DummyModel
from marshmallow import ValidationError
from flask import request
from flask_jwt_extended import (get_jwt_identity,
                                get_jwt_claims,
                                jwt_required
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

############################
### POST new entry depend on user-identity
############################
    @jwt_required
    def post(self):
        dummy_json = request.get_json()
        user_id = get_jwt_identity()
        dummy_json["user_id"]=user_id
        dummy_json["dummy_active"]=False

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

        change_dummy = DummyModel.query.filter_by(id=dummy_json["id"]).first()

        if change_dummy is None or change_dummy.user_id != user_id:
             return {'message': 'No right credintials to change'}, 400

        try:
            change_dummy.string = dummy_json["string"]
            change_dummy.int_zahl = dummy_json["int_zahl"]
            change_dummy.float_zahl = dummy_json["float_zahl"]
            change_dummy.bool = dummy_json["bool"]
            change_dummy.text = dummy_json["text"]
            change_dummy.user_id = dummy_json["user_id"]
        except:
            return {'message': 'alle felder belegen'}, 400

        change_dummy.save_to_db()

        return dummy_schema.dump(change_dummy), 200

############################
### Archive a existing entry depend on user-identity
############################
    @jwt_required
    def delete(self):
        dummy_json = request.get_json()
        user_id = get_jwt_identity()

        change_dummy = DummyModel.query.filter_by(id=dummy_json["id"]).first()

        if change_dummy is None or change_dummy.user_id != user_id:
             return {'message': 'No right credintials to change'}, 400
        try:
            change_dummy.dummy_active = False
        except:
            return {'message': 'ID angeben'}, 400

        change_dummy.save_to_db()

        return {'message': 'Deleted'}, 200


class DummyList(Resource):
############################
### GET all Entries
############################
    @jwt_required
    def get(self):

        # filter by where dummy_active == True

        return {'message': dummy_schema_list.dump(DummyModel.query.all())}, 200
