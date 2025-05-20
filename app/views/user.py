from flask import jsonify, request
from app.views import api
from app.models import User
from app import db
from app.schemas import UserSchema
from marshmallow import ValidationError

user_schema = UserSchema()

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

@api.route('/user', methods=['POST'])
def create_user():
    try:
        data = user_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    
    user = User(name=data['name'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user_schema.dump(user)), 201

@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify(user_schema.dump(users, many=True)) 