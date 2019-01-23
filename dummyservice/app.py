from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import config
from models.dummy import DummyModel
from resources.dummy import Dummy, DummyList
from db import db
from ma import ma

app = Flask(__name__)

############################
### LOAD CONFIGRUATION
############################
app.config.from_object(config.DevelopmentConfig)

db.init_app(app)
ma.init_app(app)

api = Api(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

############################
### ADD REST API ENDPOINTS
############################
# USER Endpoints
api.add_resource(DummyList, '/pch/dummy/v1')
api.add_resource(Dummy, '/pch/dummy/v1/add')
# ADMIN Endpoints


if __name__ == '__main__':
    app.run()
