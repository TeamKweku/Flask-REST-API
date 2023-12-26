from flask import request
import uuid
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_smorest import Blueprint, abort
from flask_jwt_extended import  jwt_required
from flask.views import MethodView
from schema import ShopSchema, ShopUpdateSchema
from models import ShopModel
from db import db



blueprint = Blueprint("shops", __name__, description="Operations on shops")

@blueprint.route("/shop/<shop_id>")
class Shop(MethodView):
    @blueprint.response(200, ShopSchema)
    @jwt_required()
    def get(self, shop_id):
        # try:
        #     return shops[shop_id]
        # except KeyError:
        #     abort(404, message="Shop not found")
        shop = ShopModel.query.get_or_404(shop_id)
        return shop

    @jwt_required()
    def delete(self, shop_id):
        # try:
        #     del shops[shop_id]
        #     return {"message": "Shop deleted"}
        # except KeyError:
        #     abort(404, message="Shop not found")
        shop = ShopModel.query.get_or_404(shop_id)
        db.session.delete(shop)

        
        return {"message": "Shop deleted"}

    @jwt_required()
    @blueprint.arguments(ShopUpdateSchema)
    @blueprint.response(201, ShopUpdateSchema)
    
    def put(self, shop_data ,shop_id):
        # shop_data = request.json
        # if "price" not in shop_data or "name" not in shop_data:
        #     abort(400, message="Shop can't be updated")
        # try:   
        #     shop = shops[shop_id]
        #     shop.update(shop_data)
        #     return shop
        # except KeyError:
        #     abort(404, message="Shop not found")

        shop = ShopModel.query.get_or_404(shop_id)
        if shop:
            shop.name = shop_data["name"]
        else:
            shop = ShopModel(id=shop_id, **shop_data)
        try:
            db.session.add(shop)
            db.session.commit()

        except SQLAlchemyError:
            abort(500, message="Error updating shop")


@blueprint.route("/shop")
class ShopList(MethodView):
    @jwt_required()
    @blueprint.response(200, ShopSchema(many=True)) # many=True -> means its a list
    def get(self):
        # return list(shops.values())
        shops = ShopModel.query.all()
        return shops

    @jwt_required()
    @blueprint.arguments(ShopSchema)
    @blueprint.response(200, ShopSchema)
    def post(self, shop_data):
        # shop_data = request.json

        # if "name" not in shop_data:
        #     abort(400, message="Name field required")
        shop = ShopModel(**shop_data)
        # for shop in shops.values():
        #     if shop_data["name"] == shop["name"]:
        #         abort(400, message="Shop already exists")  
        # shop_id = uuid.uuid4().hex
        # shop = {**shop_data, "id": shop_id}
        # shops[shop_id] = shop
        try:
            db.session.add(shop)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Shop name must be unique")
        except SQLAlchemyError:
            abort(500, message="Error adding shop to database")

        return shop