# from flask import Blueprint
from flask import  Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os
from functools import wraps
from datetime import datetime, timedelta
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

# Import the SQLAlchemy models and schemas
from main.modules.user.models import db, BusinessBase, IdeaHolderBase, ProductChain,Requirement,Supplie,UserBase
from main.modules.user.schemas import BusinessBaseSchema, IdeaHolderBaseSchema
idea_holder_base_schema = IdeaHolderBaseSchema()
idea_holder_base_list_schema = IdeaHolderBaseSchema(many=True)


blueprint = Blueprint('user', __name__, url_prefix='/api')

SECRET_KEY= 'microhack2023'

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Check if an 'Authorization' header is present in the request
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        # Return an error response if no token is found
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            # Decode the token using the secret key
            data = jwt.decode(token, 'qlTn0bKAHYwxXAQA2jqLzjuiM9ueyL', algorithms=["HS256"])
            current_user = None
            # Check if the decoded token contains a 'business_id' key
            if 'business_id' in data:
                # Query the BusinessBase table for a user with the matching ID
                current_user = BusinessBase.query.filter_by(id=data['business_id']).first()
            # Check if the decoded token contains an 'ideaholder_id' key
            elif 'ideaholder_id' in data:
                # Query the IdeaHolderBase table for a user with the matching ID
                current_user = IdeaHolderBase.query.filter_by(id=data['ideaholder_id']).first()
            # Return an error response if the user is not found
            if not current_user:
                return jsonify({'message': 'Invalid token!'}), 401
        except jwt.ExpiredSignatureError:
            # Return an error response if the token is expired
            return jsonify({'message': 'Token has expired!'}), 401
        except (jwt.InvalidTokenError, Exception):
            # Return an error response if the token is invalid or cannot be decoded
            return jsonify({'message': 'Invalid token!'}), 401
        # Pass the authenticated user to the decorated function
        return f(current_user, *args, **kwargs)
    return decorated


# Define a helper function for checking if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ideaholder api
@blueprint.route('/ideaholder/signup', methods=['POST'])
def ideaholder_signup():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    ideaholder = IdeaHolderBase(username=data['username'], email=data['email'], password=hashed_password, budget=data['budget'], productionquantity=data['productionquantity'])
    db.session.add(ideaholder)
    db.session.commit()
    token = jwt.encode({'id': ideaholder.id, 'exp': datetime.utcnow() + timedelta(hours=24)}, SECRET_KEY)
    return jsonify({'token': token.decode('UTF-8')})



@blueprint.route('/ideaholder/authenticate', methods=['POST'])
def ideaholder_authenticate():
    data = request.get_json()
    ideaholder = IdeaHolderBase.query.filter_by(email=data['email']).first()
    if not ideaholder:
        return jsonify({'message': 'Invalid email or password'})
    if check_password_hash(ideaholder.password, data['password']):
        token = jwt.encode({'id': ideaholder.id, 'exp': datetime.utcnow() + timedelta(hours=24)}, SECRET_KEY)
        return jsonify({'token': token.decode('UTF-8')})
    return jsonify({'message': 'Invalid email or password'})


@blueprint.route('/ideaholder/idea_holder_bases', methods=['GET'])
def get_idea_holder_bases():
    idea_holder_bases = IdeaHolderBase.query.all()
    return idea_holder_base_list_schema.jsonify(idea_holder_bases)

@blueprint.route('/ideaholder/idea_holder_bases/<int:idea_holder_base_id>', methods=['GET'])
def get_idea_holder_base(idea_holder_base_id):
    idea_holder_base = IdeaHolderBase.query.get_or_404(idea_holder_base_id)
    return idea_holder_base_schema.jsonify(idea_holder_base)

@blueprint.route('/ideaholder/idea_holder_bases', methods=['POST'])
def create_idea_holder_base():
    try:
        idea_holder_base = idea_holder_base_schema.load(request.json, session=db.session)
        db.session.add(idea_holder_base)
        db.session.commit()
        return idea_holder_base_schema.jsonify(idea_holder_base), 201
    except ValidationError as e:
        return jsonify(e.messages), 400
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': 'Email already exists.'}), 400

@blueprint.route('/ideaholder/idea_holder_bases/<int:idea_holder_base_id>', methods=['PUT'])
def update_idea_holder_base(idea_holder_base_id):
    idea_holder_base = IdeaHolderBase.query.get_or_404(idea_holder_base_id)
    try:
        idea_holder_base = idea_holder_base_schema.load(request.json, instance=idea_holder_base, session=db.session)
        db.session.commit()
        return idea_holder_base_schema.jsonify(idea_holder_base)
    except ValidationError as e:
        return jsonify(e.messages), 400
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': 'Email already exists.'}), 400

@blueprint.route('/ideaholder/idea_holder_bases/<int:idea_holder_base_id>', methods=['DELETE'])
def delete_idea_holder_base(idea_holder_base_id):
    idea_holder_base = IdeaHolderBase.query.get_or_404(idea_holder_base_id)
    db.session.delete(idea_holder_base)
    db.session.commit()
    return '', 204

#business api
@blueprint.route('/business/signup', methods=['POST'])
def business_signup():
    data = request.form
    hashed_password = generate_password_hash(data['password'], method='sha256')
    logo = request.files['logo']
    filename = secure_filename(logo.filename)
    logo.save(os.path.join(UPLOAD_FOLDER, filename))
    business = BusinessBase(username=data['username'], email=data['email'], password=hashed_password, logo=filename, industry=data['industry'], location=data['location'], companySize=data['companySize'], incomeSize=data['incomeSize'], public=data['public'])
    db.session.add(business)
    db.session.commit()
    token = jwt.encode({'id': business.id, 'exp': datetime.utcnow() + timedelta(hours=24)}, SECRET_KEY)
    return jsonify({'token': token.decode('UTF-8')})

@blueprint.route('/business/authenticate', methods=['POST'])

def business_authenticate():
    data = request.get_json()
    business = BusinessBase.query.filter_by(email=data['email']).first()
    if not business:
        return jsonify({'message': 'Invalid email or password'})
    if check_password_hash(business.password, data['password']):
        token = jwt.encode({'id': business.id, 'exp': datetime.utcnow() + timedelta(hours=24)}, SECRET_KEY)
        return jsonify({'token': token.decode('UTF-8')})
    return jsonify({'message': 'Invalid email or password'})


@blueprint.route('/businesses/<int:id>', methods=['GET'])
def get_business(id):
    business = BusinessBase.query.get(id)
    if business:
        result = BusinessBaseSchema.dump(business)
        return jsonify(result)
    return jsonify({'message': 'Business not found'}), 404


@blueprint.route('/businesses/<int:id>', methods=['PUT'])
def update_business(id):
    business = BusinessBase.query.get(id)
    if business:
        try:
            updated_business = BusinessBaseSchema.load(request.json, session=db.session, instance=business)
            db.session.commit()
            result = BusinessBaseSchema.dump(updated_business)
            return jsonify(result)
        except ValidationError as e:
            return jsonify({'message': str(e)}), 400
    return jsonify({'message': 'Business not found'}), 404


@blueprint.route('/businesses/<int:id>', methods=['DELETE'])
def delete_business(id):
    business = BusinessBase.query.get(id)
    if business:
        db.session.delete(business)
        db.session.commit()
        return '', 204
    return jsonify({'message': 'Business not found'}), 404





