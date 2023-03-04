
from flask import  Blueprint, request, jsonify

from main.modules.product.models import FitBusPro,ProductBase,ProductFitBase

from main.modules.product.schemas import FitBusProSchema,ProductBaseSchema,ProductFitBaseSchema

blueprint = Blueprint('product', __name__, url_prefix='/api')




@blueprint.route('/getchain', methods=['POST'])
def chain():
    data = request.get_json()
    return {'data' : data, 'msg': 'success'}