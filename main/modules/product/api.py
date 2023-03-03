
from flask import Blueprint

from main.modules.product.models import FitBusPro,ProductBase,ProductFitBase

from main.modules.product.schemas import FitBusProSchema,ProductBaseSchema,ProductFitBaseSchema

blueprint = Blueprint('product', __name__, url_prefix='/api')
