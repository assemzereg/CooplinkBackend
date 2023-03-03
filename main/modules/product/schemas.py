from marshmallow import Schema, fields



class FitBusProSchema(Schema):
    business_id = fields.Integer(required=True)
    product_id = fields.Integer(required=True)


class ProductBaseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    # quantityPerHour = fields.Float(required=True)
    productionPerHour = fields.String(required=True)
    price = fields.Integer(required=True)
    quality = fields.String(required=True)


class ProductFitBaseSchema(Schema):
    id = fields.Integer(dump_only=True)
    product_id = fields.Integer(required=True)
    business_chain = fields.List(fields.Nested('BusinessBaseSchema'))
    associated_product = fields.Nested('ProductBaseSchema')