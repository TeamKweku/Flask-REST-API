from flask import request
import uuid
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from db import shops 
from schema import ShopSchema, ShopUpdateSchema


blueprint = Blueprint("shops", __name__, description="Operations on shops")

@blueprint.route("/shop/<shop_id>")
class Shop(MethodView):
    def get(self, shop_id):
        try:
            return shops[shop_id]
        except KeyError:
            abort(404, message="Shop not found")

    def delete(self, shop_id):
        try:
            del shops[shop_id]
            return {"message": "Shop deleted"}
        except KeyError:
            abort(404, message="Shop not found")

    @blueprint.arguments(ShopUpdateSchema)
    def put(self, shop_data ,shop_id):
        # shop_data = request.json
        # if "price" not in shop_data or "name" not in shop_data:
        #     abort(400, message="Shop can't be updated")
        try:   
            shop = shops[shop_id]
            shop.update(shop_data)
            return shop
        except KeyError:
            abort(404, message="Shop not found")

@blueprint.route("/shop")
class ShopList(MethodView):
    def get(self):
        return {"shops": list(shops.values())}

    @blueprint.arguments(ShopSchema)
    def post(self, shop_data):
        # shop_data = request.json

        # if "name" not in shop_data:
        #     abort(400, message="Name field required")

        for shop in shops.values():
            if shop_data["name"] == shop["name"]:
                abort(400, message="Shop already exists")  
        shop_id = uuid.uuid4().hex
        shop = {**shop_data, "id": shop_id}
        shops[shop_id] = shop

        return shop