"""
Steps to receive username and password from the client (as JSON)
    1. Check if a user with that username already exits
    2. If it doesn't...
        - Encrypt the password
        - Add a new UserModel to the database
        - Return a success message
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256

from db import db
from models import UserModel
from schema import UserSchema

blueprint = Blueprint("Users", "users", description="Operations on users")


@blueprint.route("/register")
class UserRegister(MethodView):
    @blueprint.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            # abort 409 means conflicting request
            abort(409, message="A username provided already exits")
             
            user = UserModel(username=user_data["username"],
                             password=pbkdf2_sha256.hash(user_data["password"]))
            db.session.add(user)
            db.session.commit()

            return {"message": "User created successfully"}, 201
    
    # For development purpose to chech created users
    @blueprint.response(200, UserSchema(many=True))
    def get(self):
        users = UserModel.query.all()

        return users