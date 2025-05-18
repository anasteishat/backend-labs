from flask import jsonify, request
from app.views import api

users = {}

@api.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

@api.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    user = users[user_id]
    del users[user_id]
    return jsonify(user)

@api.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    new_id = max(users.keys()) + 1 if users else 1
    
    user = {
        'id': new_id,
        'name': data['name']
    }
    users[new_id] = user
    
    return jsonify(user), 201

@api.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values())) 