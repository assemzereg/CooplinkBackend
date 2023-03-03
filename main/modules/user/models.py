from enum import unique
from main.extensions import db
from main.shared.base_model import BaseModel, HasCreatedAt, HasUpdatedAt



class UserBase(BaseModel, HasCreatedAt, HasUpdatedAt):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)



class BusinessBase(UserBase):
    __tablename__ = 'buisnesses'
    logo = db.Column(db.String)
    industry= db.Column(db.String, nullable=False)
    location= db.Column(db.String, nullable=False)
    companySize= db.Column(db.CHAR, nullable=False)
    incomeSize= db.Column(db.CHAR, nullable=False)
    # lacking product supply


class IdeaHolderBase(UserBase):
    __tablename__='ideaholders'
    budget = db.Column(db.Integer, nullable=False)
    productionquantity= db.Column(db.Integer, nullable=False)
    #lacking product requirements
    #laking production chain

