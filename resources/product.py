from flask import request
import uuid
from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import Blueprint, abort

# proctecting endpoints using jwt_required
from flask_jwt_extended import  jwt_required

from flask.views import MethodView
from db import db
from models import ProductModel, ShopModel
from schema import ProductSchema, ProductUpdateSchema

blueprint = Blueprint("products", __name__, description="Operations on products")

@blueprint.route("/product")
class ProductList(MethodView):
    @jwt_required()
    @blueprint.response(200, ProductSchema(many=True))
    def get(self):
        products = ProductModel.query.all()

        return products

    @jwt_required()
    @blueprint.arguments(ProductSchema)
    @blueprint.response(200, ProductSchema)
    def post(self, product_data):
        # product_data = request.json

        # if "name" not in product_data:
        #     abort(400, message="Name field required")
        product = ProductModel(**product_data)
        # for product in products.values():
        #     if product_data["name"] == product["name"]:
        #         abort(400, message="product already exists")  
        # product_id = uuid.uuid4().hex
        # product = {**product_data, "id": product_id}
        # products[product_id] = product
        try:
            db.session.add(product)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error inserting product")


        return product


@blueprint.route("/product/<product_id>")
class Product(MethodView):
    @jwt_required()
    @blueprint.response(200, ProductSchema)
    def get(self, product_id):
        # return products[product_id]
        product = ProductModel.query.get_or_404(product_id)
        return product
        
        # except KeyError:
        #     abort(404, message="product not found")
    @jwt_required()
    def delete(self, product_id):
        # try:
        #     return {"message": "product deleted"}
        # except KeyError:
        #     abort(404, message="product not found")
        product = ProductModel.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()

        return {"message": "Product deleted"}
    
    @jwt_required()
    @blueprint.arguments(ProductUpdateSchema)
    @blueprint.response(201, ProductUpdateSchema)
    
    def put(self, product_data, product_id):
        # product_data = request.json
        # if "price" not in product_data or "name" not in product_data:
        #     abort(400, message="product can't be updated")
        # try:   
        #     # product = products[product_id]
        #     # product.update(product_data)
        
        # except KeyError:
        #     abort(404, message="product not found")
        print(product_data)
        print(product_id)

        product = ProductModel.query.get_or_404(product_id)
        # if product:
        #     product.price = product_data["price"]
        #     product.price = product_data["@jwt_required()name"]
        # else:
        #     product = ProductModel(id=product_id, **product_data)

        # Update only the fields provided in the request
        for key, value in product_data.items():
            setattr(product, key, value)

        try:
            # db.session.add(product)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error updating product")

        return product
    
# Listing projects by shop id
@blueprint.route('/shop/<int:shop_id>/products')
class ProductsByShop(MethodView):
    @jwt_required()
    @blueprint.response(200, ProductSchema(many=True))
    def get(self, shop_id):
        # Fetch products for the given shop_id
        products = ProductModel.query.filter_by(shop_id=shop_id).all()

        # shop = ShopModel.query.get_or_404(shop_id)

        # # Fetch products for the given shop
        # products = shop.products.all()

        if not products:
            abort(404, message="No products found for this shop")

        return products