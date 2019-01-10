from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from db import db
from models.dummy import DummyModel
from resources.dummy import Dummy, DummyList
import config
from flask_jwt_extended import JWTManager

app = Flask(__name__)

############################
### LOAD CONFIGRUATION
############################
app.config.from_object(config.DevelopmentConfig)

db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

############################
### ADD REST API ENDPOINTS
############################
api.add_resource(DummyList, '/pch/dummy/v1')
api.add_resource(Dummy, '/pch/dummy/v1/add')

if __name__ == '__main__':
    app.run()
