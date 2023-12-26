import os
from flask import Flask, request, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from resources.shop import blueprint as ShopBlueprint
from resources.product import blueprint as ProductBlueprint
from resources.user import blueprint as UserBlueprint
from flask_migrate import Migrate
import uuid
from db import db
import models
from blacklist import BLACKLIST

app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "My API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#JWT config
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

migrate = Migrate(app, db)
jwt = JWTManager(app)

# Handle errors that arises with JWT tokens
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLACKLIST

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (jsonify({"message": "Token has been revoked",
                     "error": "revoked_token"}), 401)

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (jsonify({"message": "Provided token expired",
                     "error": "token_expired"}), 401)

@jwt.invalid_token_loader
def invalid_token_loader_callback(error):
    return (jsonify({"message": "Signature verification failed",
                     "error": "invalid_token"}), 401)

@jwt.unauthorized_loader
def missing_token_callback(error):
    return (jsonify({"message": "Request doesn't contain an access token",
                     "error": "authorization required"}), 401)

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return (jsonify({"message": "The token is not a fresh token",
                     "error": "fresh_token_required"}), 401)


db.init_app(app)

api = Api(app)

# with app.app_context():
#     db.create_all()

api.register_blueprint(ShopBlueprint)
api.register_blueprint(ProductBlueprint)
api.register_blueprint(UserBlueprint)