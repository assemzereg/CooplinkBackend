from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from app import db
from models import Supplie, Requirement, ProductChain, BusinessBase, IdeaHolderBase
from main.modules.product.models import ProductBase

class SupplieSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Supplie
        sqla_session = db.session
        load_instance = True


class RequirementSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Requirement
        sqla_session = db.session
        load_instance = True


class ProductChainSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ProductChain
        sqla_session = db.session
        load_instance = True


class BusinessBaseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BusinessBase
        sqla_session = db.session
        load_instance = True

    # Include related supplies in the output
    supplies = fields.Nested('ProductSchema', many=True)


class IdeaHolderBaseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = IdeaHolderBase
        sqla_session = db.session
        load_instance = True

    # Include related requirements and product_chain in the output
    requirements = fields.Nested('ProductSchema', many=True)
    product_chain = fields.Nested('BusinessBaseSchema', many=True)


class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ProductBase
        sqla_session = db.session
        load_instance = True
