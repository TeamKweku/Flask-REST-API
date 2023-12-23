from flask import request
import uuid
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from db import products
from schema import ProductSchema, ProductUpdateSchema

blueprint = Blueprint("products", __name__, description="Operations on products")

@blueprint.route("/product")
class ProductList(MethodView):
    @blueprint.response(200, ProductSchema(many=True))
    def get(self):
        return {"products": list(products.values())}

    @blueprint.arguments(ProductSchema)
    @blueprint.response(200, ProductSchema)
    def post(self, product_data):
        # product_data = request.json

        # if "name" not in product_data:
        #     abort(400, message="Name field required")

        for product in products.values():
            if product_data["name"] == product["name"]:
                abort(400, message="product already exists")  
        product_id = uuid.uuid4().hex
        product = {**product_data, "id": product_id}
        products[product_id] = product

        return product

@blueprint.route("/product/<product_id>")
class Product(MethodView):
    @blueprint.response(200, ProductSchema)
    def get(self, product_id):
        try:
            return products[product_id]
        except KeyError:
            abort(404, message="product not found")

    def delete(self, product_id):
        try:
            del products[product_id]
            return {"message": "product deleted"}
        except KeyError:
            abort(404, message="product not found")

    @blueprint.arguments(ProductUpdateSchema)
    @blueprint.response(201, ProductUpdateSchema)
    def put(self, product_data, product_id):
        # product_data = request.json
        # if "price" not in product_data or "name" not in product_data:
        #     abort(400, message="product can't be updated")
        try:   
            product = products[product_id]
            product.update(product_data)
            return product
        except KeyError:
            abort(404, message="product not found")
