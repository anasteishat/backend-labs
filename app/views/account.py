from flask import jsonify, request
from app.views import api
from app.models import Account, User
from app import db
from app.schemas import account_schema, balance_update_schema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

@api.route('/account/<int:account_id>', methods=['GET'])
def get_account(account_id):
    account = Account.query.get(account_id)
    if account is None:
        return jsonify({'error': 'Account not found'}), 404
    return jsonify(account_schema.dump(account))

@api.route('/account', methods=['POST'])
def create_account():
    try:
        data = account_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    
    user = User.query.get(data['user_id'])
    if user is None:
        return jsonify({'error': 'User not found'}), 400
    
    if Account.query.filter_by(user_id=data['user_id']).first():
        return jsonify({'error': 'User already has an account'}), 400
    
    try:
        account = Account(
            user_id=data['user_id'],
            balance=data['balance']
        )
        db.session.add(account)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500
    
    return jsonify(account_schema.dump(account)), 201

@api.route('/account/<int:account_id>/balance', methods=['PUT'])
def update_balance(account_id):
    try:
        data = balance_update_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    account = Account.query.get(account_id)
    if account is None:
        return jsonify({'error': 'Account not found'}), 404

    try:
        account.increase_balance(data['amount'])
        db.session.commit()
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500

    return jsonify(account_schema.dump(account))

@api.route('/account/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    account = Account.query.get(account_id)
    if account is None:
        return jsonify({'error': 'Account not found'}), 404
    
    try:
        db.session.delete(account)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Cannot delete account with existing records'}), 400
    
    return '', 204 