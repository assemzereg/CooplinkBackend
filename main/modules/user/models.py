from enum import unique
from main.extensions import db
from main.shared.base_model import BaseModel, HasCreatedAt, HasUpdatedAt

class Supplie(BaseModel):
    __tablename__ = 'supplies'

    business_id = db.Column(db.Integer, db.ForeignKey(
        'businesses.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), primary_key=True)

class Requirement(BaseModel):
    __tablename__ = 'requirements'

    ideaholder_id = db.Column(db.Integer, db.ForeignKey(
        'ideaholders.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), primary_key=True)

class ProductChain(BaseModel,HasCreatedAt, HasUpdatedAt):
    __tablename__ = 'product_chain'

    Productfit_id = db.Column(db.Integer, db.ForeignKey(
        'productfits.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), primary_key=True)

 
class UserBase(BaseModel, HasCreatedAt, HasUpdatedAt):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)



class BusinessBase(UserBase):
    __tablename__ = 'businesses'
    logo = db.Column(db.String)
    industry= db.Column(db.String, nullable=False)
    location= db.Column(db.String, nullable=False)
    companySize= db.Column(db.CHAR, nullable=False)
    incomeSize= db.Column(db.CHAR, nullable=False)
    public= db.Column(db.Boolean, nullable=False)
    supplies= db.relationship(
        'ProductBase', secondary='supplies', backref=db.backref('businesses', lazy='dynamic'))



class IdeaHolderBase(UserBase):
    __tablename__='ideaholders'
    budget = db.Column(db.Integer, nullable=False)
    productionquantity= db.Column(db.Integer, nullable=False)
    requirements= db.relationship(
        'ProductBase', secondary='requirements', backref=db.backref('ideaholders', lazy='dynamic'))
    chain = db.relationship('ProductFitBase', secondary='product_chain', backref=db.backref('ideaholders', lazy='dynamic'))

