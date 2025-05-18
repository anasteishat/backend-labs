from flask import jsonify, request
from app.views import api

categories = {}

@api.route('/category/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = categories.get(category_id)
    if category is None:
        return jsonify({'error': 'Category not found'}), 404
    return jsonify(category)

@api.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    if category_id not in categories:
        return jsonify({'error': 'Category not found'}), 404
    category = categories[category_id]
    del categories[category_id]
    return jsonify(category)

@api.route('/category', methods=['POST'])
def create_category():
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    new_id = max(categories.keys()) + 1 if categories else 1
    
    category = {
        'id': new_id,
        'name': data['name']
    }
    categories[new_id] = category
    
    return jsonify(category), 201