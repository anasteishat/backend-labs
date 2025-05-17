from flask import Blueprint, jsonify

api = Blueprint('api', __name__)

@api.route('/health')
def healthcheck():
    return jsonify({"status": "healthy"}), 200 