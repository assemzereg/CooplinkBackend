from flask import Flask, Blueprint, request
from main.model.prediction import predict
from main.extensions import db, migrate, cors, jwt
from main.settings import DevSettings
# from flask_jwt_extended import JWTManager
import click
from flask.cli import with_appcontext

from main.modules.user.models import BusinessBase
from main.modules.product.models import ProductBase

from main.modules import user, product
import string
import random

MODULES = [user, product]


main = Blueprint('main', __name__)


def create_app(settings=DevSettings):
    app = Flask(__name__)
    app.config['SECRET_KEY']= 'microhack2023'
    # Setup the Flask-JWT-Extended extension
    app.config["JWT_SECRET_KEY"] = "qlTn0bKAHYwxXAQA2jqLzjuiM9ueyL"
    # jwt = JWTManager(app)

    # Utiliser la configuration (settings).
    app.config.from_object(settings)
    # On initialise les libraries Python.
    # Init SQLAlchemy.
    db.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)

    # Init Migrate.
    migrate.init_app(app, db)
    app.register_blueprint(main)
    # register_modules(app)
    register_shell_context(app)
    # populate_businesses()

    return app


def register_shell_context(app):
    def shell_context():
        return {'db': db}
    app.shell_context_processor(shell_context)


def register_modules(app):
    for m in MODULES:
        if hasattr(m, 'api'):
            app.register_blueprint(m.api)

# @click.command('populate:businesses')
# @with_appcontext
# def populate_businesses():
#     business = {'id': 0, 'username': 'matprem', 'email': 'matprem', 'password': '', 'industry' : 'human ressources', 'location': 'Algiers', 'companySize': '', 'incomeSize': '', 'public': True}
#     # product = ProductBase.query.filter_by(name='Fer').first()
#     new_product = ProductBase(name='New Product', productionPerHour='10', price=100, quality='H')
#     db.session.add(new_product)
#     db.session.commit()
#     for i in range(82, 110):
#         # b = {'id': business['id']+i, 'username': business['username']+str(i), 'email': business['email']+str(i)+'@gmail.com', 'password': "".join(random.choice(string.ascii_letters + string.digits) for i in range(10)), 'industry' : business['industry'], 'location': 'Algiers', 'companySize': random.choice(['L','M','S']), 'incomeSize': random.choice(['H','A','L']), 'public': True , 'supplies' :None}
#         new_business = BusinessBase({'id': business['id']+i, 'username': business['username']+str(i), 'email': business['email']+str(i)+'@gmail.com', 'password': "".join(random.choice(string.ascii_letters + string.digits) for i in range(10)), 'industry' : business['industry'], 'location': 'Algiers', 'companySize': random.choice(['L','M','S']), 'incomeSize': random.choice(['H','A','L']), 'public': True })
#         new_business.supplies.append(new_product)
#         db.session.add(new_business)
#         db.session.commit()
#     print('business populated')
    # click.echo('Diets successfully populated.')

@main.route('/getchain', methods=['POST'])
def getchain():
    data = request.get_json()
    price_unit=(data['budget']/len(data['products_list']))/data['mass']
    if price_unit<1:
        return {'data': [], 'msg': 'budget too low'}
    print('data',data)
    result = predict(budjet=data['budget'], mass=data['mass'], products=data['prod'])

    return {'data' : result, 'msg': 'success'}


@main.route('/')
@main.route('/index')
def index():
    return 'First Page, Ici sera notre projet.'
