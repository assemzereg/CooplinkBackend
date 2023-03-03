from marshmallow import Schema, fields

class SupplySchema(Schema):
    business_id = fields.Integer(required=True)
    product_id = fields.Integer(required=True)


class RequirementSchema(Schema):
    ideaholder_id = fields.Integer(required=True)
    business_id = fields.Integer(required=True)


class ProductChainSchema(Schema):
    Productfit_id = fields.Integer(required=True)
    product_id = fields.Integer(required=True)


class UserBaseSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)


class BusinessBaseSchema(UserBaseSchema):
    logo = fields.String()
    industry = fields.String(required=True)
    location = fields.String(required=True)
    companySize = fields.String(required=True)
    incomeSize = fields.String(required=True)
    public = fields.Boolean(required=True)
    supplies = fields.List(fields.Nested('ProductBaseSchema'))


class IdeaHolderBaseSchema(UserBaseSchema):
    budget = fields.Integer(required=True)
    productionquantity = fields.Integer(required=True)
    requirements = fields.List(fields.Nested('ProductBaseSchema'))
    chain = fields.List(fields.Nested('ProductFitBaseSchema'))


