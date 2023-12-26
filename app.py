import os
from flask import Flask, request
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from resources.shop import blueprint as ShopBlueprint
from resources.product import blueprint as ProductBlueprint
from resources.user import blueprint as UserBlueprint
from flask_migrate import Migrate
import uuid
from db import db
import models

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

db.init_app(app)

api = Api(app)

# with app.app_context():
#     db.create_all()

api.register_blueprint(ShopBlueprint)
api.register_blueprint(ProductBlueprint)
api.register_blueprint(UserBlueprint)