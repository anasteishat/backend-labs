from flask import jsonify, request
from datetime import datetime
from app.views import api

records = {}

@api.route('/record/<int:record_id>', methods=['GET'])
def get_record(record_id):
    record = records.get(record_id)
    if record is None:
        return jsonify({'error': 'Record not found'}), 404
    return jsonify(record)

@api.route('/record/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    if record_id not in records:
        return jsonify({'error': 'Record not found'}), 404
    record = records[record_id]
    del records[record_id]
    return jsonify(record)

@api.route('/record', methods=['POST'])
def create_record():
    data = request.get_json()
    
    required_fields = ['user_id', 'category_id', 'price']
    for field in required_fields:
        if not data or field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    new_id = max(records.keys()) + 1 if records else 1
    
    record = {
        'id': new_id,
        'user_id': data['user_id'],
        'category_id': data['category_id'],
        'datetime': datetime.now().isoformat(),
        'price': data['price']
    }
    records[new_id] = record
    
    return jsonify(record), 201

@api.route('/record', methods=['GET'])
def get_records():
    user_id = request.args.get('user_id', type=int)
    category_id = request.args.get('category_id', type=int)
    
    if not user_id and not category_id:
        return jsonify({'error': 'Either user_id or category_id (or both) must be provided'}), 400
    
    filtered_records = []
    for record in records.values():
        if user_id and category_id:
            if record['user_id'] == user_id and record['category_id'] == category_id:
                filtered_records.append(record)
        elif user_id and record['user_id'] == user_id:
            filtered_records.append(record)
        elif category_id and record['category_id'] == category_id:
            filtered_records.append(record)
    
    return jsonify(filtered_records) 