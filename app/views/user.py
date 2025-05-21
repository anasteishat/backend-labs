from flask import jsonify, request
from app.views import api
from app.models import User
from app import db
from app.schemas import UserSchema
from marshmallow import ValidationError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token

user_schema = UserSchema()

@api.route('/register', methods=['POST'])
def register_user():
    try:
        data = user_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    
    existing_user = User.query.filter_by(name=data['name']).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 400
    
    user = User(
        name=data['name'],
        password=pbkdf2_sha256.hash(data['password'])
    )
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user_schema.dump(user)), 201

@api.route('/login', methods=['POST'])
def login_user():
    try:
        data = request.get_json()
    except Exception as err:
        return jsonify({'error': 'Invalid request data'}), 400
    
    user = User.query.filter_by(name=data['name']).first()
    if not user or not pbkdf2_sha256.verify(data['password'], user.password):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}, 200)

@api.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user_schema.dump(user))

@api.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify(user_schema.dump(user))

@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify(user_schema.dump(users, many=True)) 