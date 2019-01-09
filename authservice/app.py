from flask import Flask
from flask_restful import Api
from db import db
from resources.user import UserRegister, UserLogin, UserLogout, User
from resources.token import TokenRefresh, CheckToken
from models.user import UserModel
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import config

app = Flask(__name__)
###########################
### LOAD CONFIGURATION
###########################
app.config.from_object(config.DevelopmentConfig)

db.init_app(app)
api = Api(app)

with app.app_context():
  from models import *

migrate = Migrate(app, db)
jwt = JWTManager(app)

###########################
### ADD CLAIMS TO JWT-TOKEN
###########################
@jwt.user_claims_loader
def add_claims_to_access_token(user):
    user = UserModel.find_by_id(user)
    return {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_role': user.user_role
    }

###########################
### REST ENDPOINTS
###########################
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(CheckToken, "/checktoken")
api.add_resource(User, "/user/<int:user_id>")


if __name__ == '__main__':
    app.run()
