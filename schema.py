from marshmallow import Schema, fields

"""Schema for getting or creating a product"""
class PlainProductSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)

class PlainShopSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class ProductSchema(PlainProductSchema):
    shop_id = fields.Str(required=True)
    shop = fields.Nested(PlainShopSchema(), dump_only=True)


class ProductUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class ShopSchema(PlainShopSchema):
    products = fields.List(fields.Nested(PlainShopSchema()),
                           dump_only=True)

class ShopUpdateSchema(Schema):
    name = fields.Str()

class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)