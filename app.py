from flask import Flask, request
from flask_smorest import Api
from resources.shop import blueprint as ShopBlueprint
from resources.product import blueprint as ProductBlueprint
import uuid
from db import shops, products

app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "My API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)
api.register_blueprint(ShopBlueprint)
api.register_blueprint(ProductBlueprint)
