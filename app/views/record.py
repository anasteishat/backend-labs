from flask import jsonify, request
from datetime import datetime
from app.views import api
from app.models import Record, User, Category, Account
from app import db
from app.schemas import RecordSchema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required

record_schema = RecordSchema()

@api.route('/record/<int:record_id>', methods=['GET'])
def get_record(record_id):
    record = Record.query.get(record_id)
    if record is None:
        return jsonify({'error': 'Record not found'}), 404
    return jsonify(record_schema.dump(record))

@jwt_required()
@api.route('/record/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    record = Record.query.get(record_id)
    if record is None:
        return jsonify({'error': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit()
    return jsonify(record_schema.dump(record))

@jwt_required()
@api.route('/record', methods=['POST'])
def create_record():
    try:
        data = record_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    
    # Verify that user and category exist
    user = User.query.get(data['user_id'])
    if user is None:
        return jsonify({'error': 'User not found'}), 400
    
    category = Category.query.get(data['category_id'])
    if category is None:
        return jsonify({'error': 'Category not found'}), 400

    # Get user's account
    account = Account.query.filter_by(user_id=data['user_id']).first()
    if account is None:
        return jsonify({'error': 'User has no account'}), 400
    
    try:
        # Try to decrease the balance
        account.decrease_balance(data['price'])
        
        record = Record(
            user_id=data['user_id'],
            category_id=data['category_id'],
            account_id=account.id,
            price=data['price']
        )
        db.session.add(record)
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500
    
    return jsonify(record_schema.dump(record)), 201

@api.route('/record', methods=['GET'])
def get_records():
    user_id = request.args.get('user_id', type=int)
    category_id = request.args.get('category_id', type=int)
    
    if not user_id and not category_id:
        return jsonify({'error': 'Either user_id or category_id (or both) must be provided'}), 400
    
    query = Record.query
    
    if user_id:
        query = query.filter(Record.user_id == user_id)
    if category_id:
        query = query.filter(Record.category_id == category_id)
    
    records = query.all()
    return jsonify(record_schema.dump(records, many=True)) 