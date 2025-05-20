from flask import jsonify, request
from app.views import api
from app.models import Category
from app import db
from app.schemas import CategorySchema
from marshmallow import ValidationError

category_schema = CategorySchema()

@api.route('/category/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get(category_id)
    if category is None:
        return jsonify({'error': 'Category not found'}), 404
    return jsonify(category_schema.dump(category))

@api.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get(category_id)
    if category is None:
        return jsonify({'error': 'Category not found'}), 404
    
    db.session.delete(category)
    db.session.commit()
    return jsonify(category_schema.dump(category))

@api.route('/category', methods=['POST'])
def create_category():
    try:
        data = category_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    
    category = Category(name=data['name'])
    db.session.add(category)
    db.session.commit()
    
    return jsonify(category_schema.dump(category)), 201

@api.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify(category_schema.dump(categories, many=True))