from enum import unique
from main.extensions import db
from main.shared.base_model import BaseModel, HasCreatedAt, HasUpdatedAt

class FitBusPro(BaseModel):
    __tablename__='fitbuspro'
    business_id = db.Column(db.Integer, db.ForeignKey(
        'businesses.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'productfits.id'), primary_key=True)

class ProductBase(BaseModel, HasCreatedAt, HasUpdatedAt):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, nullable=True)
    # quantityPerHour= db.Column(db.String, nullable=False)
    productionPerHour= db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quality = db.Column(db.String, nullable=False)



class ProductFitBase(BaseModel):
    __tablename__='productfits'
    id = db.Column(db.Integer, primary_key=True)
    product_id= db.Column(db.Integer, db.ForeignKey('products.id'))
    business_chain = db.relationship('BusinessBase', secondary='fitbuspro', backref=db.backref('productfits', lazy='dynamic'))

    associated_product= db.relationship("ProductBase")

